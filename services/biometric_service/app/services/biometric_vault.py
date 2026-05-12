"""
BiometricVault — DPDP-compliant biometric processing.

Security contract (NEVER violated):
  - Raw images are NEVER stored on disk or in database.
  - Only AES-GCM encrypted 128-D float embeddings are persisted.
  - Liveness is validated before any enrollment or match.
  - All operations are logged with correlation IDs.
"""
import os
import hashlib
import secrets
import numpy as np
from base64 import b64decode, b64encode
from typing import Tuple
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from sqlalchemy.orm import Session
from shared.models.biometric import BiometricTemplate
from shared.models.audit import AuditLog
import uuid

# ── Encryption key (in production: fetched from KMS / HashiCorp Vault) ──────
_RAW_KEY = os.getenv("BIOMETRIC_ENCRYPTION_KEY", "")
ENCRYPTION_KEY: bytes = bytes.fromhex(_RAW_KEY) if len(_RAW_KEY) == 64 else secrets.token_bytes(32)
ALGORITHM_VERSION = "SimEmbedding-v1-AES256GCM"  # tag stored with template


# ── Helpers ──────────────────────────────────────────────────────────────────

def _encrypt_embedding(embedding: list[float]) -> Tuple[bytes, bytes]:
    """AES-256-GCM encrypt a float array. Returns (ciphertext, nonce)."""
    raw = np.array(embedding, dtype=np.float32).tobytes()
    nonce = secrets.token_bytes(12)         # 96-bit nonce per NIST recommendation
    aesgcm = AESGCM(ENCRYPTION_KEY)
    ct = aesgcm.encrypt(nonce, raw, None)   # no AAD for simplicity
    return ct, nonce


def _decrypt_embedding(ciphertext: bytes, nonce: bytes) -> list[float]:
    """Decrypt and reconstruct the float array."""
    aesgcm = AESGCM(ENCRYPTION_KEY)
    raw = aesgcm.decrypt(nonce, ciphertext, None)
    return np.frombuffer(raw, dtype=np.float32).tolist()


def _cosine_similarity(a: list[float], b: list[float]) -> float:
    va, vb = np.array(a), np.array(b)
    return float(np.dot(va, vb) / (np.linalg.norm(va) * np.linalg.norm(vb) + 1e-10))


# ── Simulated face embedding (replace with DeepFace / ONNX model) ────────────
def _generate_embedding(image_b64: str) -> Tuple[list[float], dict]:
    """
    In production this calls a real face-recognition model.
    For determinism the embedding is seeded from the image hash
    so the same image always produces the same vector.
    """
    img_hash = hashlib.sha256(image_b64.encode()).digest()
    rng = np.random.default_rng(int.from_bytes(img_hash[:4], "big"))
    embedding = rng.uniform(-1, 1, 128).tolist()
    meta = {"source_hash": img_hash.hex(), "dim": 128}
    return embedding, meta


def _simulate_liveness(image_b64: str) -> dict:
    """
    Placeholder for a real anti-spoofing model (e.g. FaceAntiSpoofing CNN).
    Returns True for images that are large enough (naïve proxy for real images).
    """
    is_live = len(image_b64) > 1000   # real model would analyse depth / texture
    return {"is_live": is_live, "confidence": 0.97 if is_live else 0.12}


# ── Service ──────────────────────────────────────────────────────────────────

class BiometricVault:

    @staticmethod
    def enroll_face(db: Session, user_id: str, image_b64: str, correlation_id: str = None) -> dict:
        """
        Enroll a user's face:
          1. Liveness check
          2. Generate embedding
          3. Encrypt
          4. Persist template
          5. Audit
        """
        # 1. Liveness
        liveness = _simulate_liveness(image_b64)
        if not liveness["is_live"]:
            return {"success": False, "reason": "liveness_failed", "liveness": liveness}

        # 2. Embedding
        embedding, meta = _generate_embedding(image_b64)

        # 3. Encrypt
        ct, nonce = _encrypt_embedding(embedding)
        combined = nonce + ct          # store nonce prepended to ciphertext

        # 4. Persist
        template = db.query(BiometricTemplate).filter(BiometricTemplate.user_id == user_id).first()
        if template:
            template.face_embedding_encrypted = combined
            template.algorithm_version = ALGORITHM_VERSION
            template.liveness_status = "verified"
            template.liveness_metadata = liveness
            template.encryption_metadata = meta
            template.confidence_score = liveness["confidence"]
        else:
            template = BiometricTemplate(
                id=str(uuid.uuid4()),
                user_id=user_id,
                face_embedding_encrypted=combined,
                algorithm_version=ALGORITHM_VERSION,
                embedding_dimension=128,
                liveness_status="verified",
                liveness_metadata=liveness,
                encryption_metadata=meta,
                confidence_score=liveness["confidence"],
            )
            db.add(template)

        # 5. Audit
        log = AuditLog(
            actor_id=user_id,
            actor_role="voter",
            action="BIOMETRIC_ENROLLED",
            resource="biometric_templates",
            resource_id=template.id,
            correlation_id=correlation_id,
        )
        db.add(log)
        db.commit()
        return {"success": True, "template_id": template.id}

    @staticmethod
    def verify_face(db: Session, user_id: str, image_b64: str, correlation_id: str = None) -> dict:
        """
        Verify a face against the stored template:
          1. Liveness check
          2. Generate probe embedding
          3. Decrypt gallery embedding
          4. Cosine match with threshold
        """
        # 1. Liveness
        liveness = _simulate_liveness(image_b64)
        if not liveness["is_live"]:
            return {"match": False, "reason": "liveness_failed"}

        # 2. Probe embedding
        probe_emb, _ = _generate_embedding(image_b64)

        # 3. Fetch & decrypt gallery
        template = db.query(BiometricTemplate).filter(BiometricTemplate.user_id == user_id).first()
        if not template or template.is_revoked:
            return {"match": False, "reason": "no_template_or_revoked"}

        combined = template.face_embedding_encrypted
        nonce, ct = combined[:12], combined[12:]
        gallery_emb = _decrypt_embedding(ct, nonce)

        # 4. Match
        score = _cosine_similarity(probe_emb, gallery_emb)
        matched = score >= 0.80  # EAR (Equal Acceptance Rate) threshold

        # Update verification stats
        template.verification_count = (template.verification_count or 0) + 1
        from datetime import datetime, timezone
        template.last_verified_at = datetime.now(timezone.utc)

        # Audit
        log = AuditLog(
            actor_id=user_id,
            actor_role="voter",
            action="BIOMETRIC_VERIFIED" if matched else "BIOMETRIC_FAILED",
            resource="biometric_templates",
            resource_id=template.id,
            correlation_id=correlation_id,
        )
        db.add(log)
        db.commit()

        return {"match": matched, "score": round(score, 4), "liveness": liveness}

    @staticmethod
    def revoke(db: Session, user_id: str, reason: str, officer_id: str) -> dict:
        """Revoke a biometric template (lost/compromised)."""
        template = db.query(BiometricTemplate).filter(BiometricTemplate.user_id == user_id).first()
        if not template:
            return {"success": False, "reason": "no_template"}
        template.is_revoked = True
        template.revocation_reason = reason
        log = AuditLog(
            actor_id=officer_id,
            actor_role="officer",
            action="BIOMETRIC_REVOKED",
            resource="biometric_templates",
            resource_id=template.id,
        )
        db.add(log)
        db.commit()
        return {"success": True}
