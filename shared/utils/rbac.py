from typing import Optional
from shared.models.user import User, ScopeType

def validate_scope(user: User, target_scope_type: str, target_scope_id: str, target_hierarchy: dict) -> bool:
    """
    Validates if a user has access to a target based on geographic hierarchy.
    
    target_hierarchy example: {
        'state_id': '...',
        'district_id': '...',
        'pc_id': '...',
        'ac_id': '...',
        'polling_booth_id': '...'
    }
    """
    # CEC and National Scope have global access
    if user.role == "chief_election_commissioner" or user.scope_type == ScopeType.NATIONAL:
        return True
    
    if not user.scope_type or not user.scope_id:
        return False

    user_scope = user.scope_type
    user_id = user.scope_id

    # Hierarchical checks
    if user_scope == ScopeType.STATE:
        return target_hierarchy.get('state_id') == user_id
    
    if user_scope == ScopeType.DISTRICT:
        return target_hierarchy.get('district_id') == user_id
    
    if user_scope == ScopeType.PC:
        return target_hierarchy.get('pc_id') == user_id
        
    if user_scope == ScopeType.AC:
        return target_hierarchy.get('ac_id') == user_id
        
    if user_scope == ScopeType.BOOTH:
        return target_hierarchy.get('polling_booth_id') == user_id or target_hierarchy.get('booth_id') == user_id

    return False
