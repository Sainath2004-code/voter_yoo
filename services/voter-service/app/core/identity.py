import hashlib
import re

def mask_aadhaar(aadhaar: str) -> str:
    """
    Mask Aadhaar number for storage in primary database.
    Format: XXXX-XXXX-1234
    """
    clean_aadhaar = re.sub(r'[^0-9]', '', aadhaar)
    if len(clean_aadhaar) != 12:
        return "Invalid Aadhaar"
    
    return f"XXXX-XXXX-{clean_aadhaar[-4:]}"

def hash_aadhaar(aadhaar: str, salt: str) -> str:
    """
    Create a secure hash of the Aadhaar number for duplicate detection.
    """
    clean_aadhaar = re.sub(r'[^0-9]', '', aadhaar)
    return hashlib.sha256((clean_aadhaar + salt).encode()).hexdigest()

def validate_aadhaar_format(aadhaar: str) -> bool:
    """
    Basic Verhoeff-check would go here, for now basic regex.
    """
    return bool(re.match(r'^[2-9]{1}[0-9]{3}[0-9]{4}[0-9]{4}$', aadhaar.replace("-", "")))
