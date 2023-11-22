"""
Module contains realizations of DTO classes using for Comment abstraction
"""
from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class UserDataDTO:
    """
    DTO class for user entity representation
    """
    username: str
    email: str
    _password: str
    name: str
    surname: str

@dataclass_json
@dataclass
class UserCriteria:
    """
    Custom type for user fields validation
    
    Args: 
        email (str): user email
        username (str): user email
    """
    email: str
    username: str