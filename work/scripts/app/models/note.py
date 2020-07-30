"""
    Note dataclass
"""
from datetime import datetime
from dataclasses import field
from dataclasses import dataclass


@dataclass
class Note:
    """
        Single element storage a like class
        Params:
            date (datetime.date): note date created
            name (str): note name
            description (str): note description
            uuid (int): database index
    """
    date: datetime.date
    name: str
    description: str
    uuid: int = field(default=-1)
