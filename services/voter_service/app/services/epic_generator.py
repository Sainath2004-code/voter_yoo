import random
import string
from sqlalchemy.orm import Session
from shared.models.voter import VoterProfile
from shared.models.geography import StateUT

class EPICGenerator:
    """
    Service to generate and validate ECI-compliant EPIC (Voter ID) numbers.
    Format: [StatePrefix][7 AlphaNumeric Characters]
    Example: ABC1234567
    """
    
    @staticmethod
    def generate_epic(db: Session, state_id: str) -> str:
        state = db.query(StateUT).filter(StateUT.id == state_id).first()
        if not state:
            raise ValueError("Invalid State ID")
            
        # Extract state prefix (e.g. 'UP' from 'Uttar Pradesh' if not set in code)
        # Using the code provided in the states_uts table
        prefix = state.code[:3].upper() # Take first 3 chars of code
        
        while True:
            # Generate 7 random alphanumeric characters
            random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))
            epic = f"{prefix}{random_suffix}"
            
            # Duplicate Prevention
            exists = db.query(VoterProfile).filter(VoterProfile.epic_number == epic).first()
            if not exists:
                return epic

    @staticmethod
    def validate_epic(epic: str) -> bool:
        """
        Validate EPIC format.
        """
        if not epic or len(epic) < 10:
            return False
        return True
