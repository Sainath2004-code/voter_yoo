import random
import string

def generate_epic_number(state_code: str) -> str:
    """
    Generate an Indian Voter ID (EPIC) Number.
    Standard Format: [3 Letters for State/Agency] [7 Random Digits]
    Example: ABC1234567
    """
    # ECI standard often starts with state-specific or agency prefix
    # We'll use the provided state_code or a default 'VTR'
    prefix = state_code.upper()[:3] if state_code else "VTR"
    if len(prefix) < 3:
        prefix = (prefix + "ABC")[:3]
    
    random_digits = ''.join(random.choices(string.digits, k=7))
    return f"{prefix}{random_digits}"

def validate_epic_number(epic: str) -> bool:
    """
    Basic validation for EPIC number format (3 Letters + 7 Digits)
    """
    if len(epic) != 10:
        return False
    return epic[:3].isalpha() and epic[3:].isdigit()
