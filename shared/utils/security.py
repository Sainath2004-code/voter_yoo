import hashlib
from cryptography.fernet import Fernet
import os

# In a real production system, this would come from a KMS/Vault
ENCRYPTION_KEY = os.getenv("AADHAAR_ENCRYPTION_KEY", Fernet.generate_key().decode())
fernet = Fernet(ENCRYPTION_KEY.encode())

def hash_aadhaar(aadhaar_num: str) -> str:
    """
    Generate a deterministic hash for duplicate checking.
    """
    return hashlib.sha256(aadhaar_num.encode()).hexdigest()

def mask_aadhaar(aadhaar_num: str) -> str:
    """
    Return masked Aadhaar (e.g., XXXX-XXXX-1234).
    """
    clean_num = "".join(filter(str.isdigit, aadhaar_num))
    if len(clean_num) != 12:
        return "Invalid Aadhaar"
    return f"XXXX-XXXX-{clean_num[-4:]}"

def encrypt_aadhaar(aadhaar_num: str) -> str:
    """
    Encrypt Aadhaar using Fernet (AES).
    """
    return fernet.encrypt(aadhaar_num.encode()).decode()

def decrypt_aadhaar(encrypted_payload: str) -> str:
    """
    Decrypt Aadhaar payload.
    """
    return fernet.decrypt(encrypted_payload.encode()).decode()
