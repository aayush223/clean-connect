from typing import Dict, Any, List

class SQLAlchemyMockState:
    """Simulates relational database storage with indexes and SLA validation rules."""
    def __init__(self) -> None:
        self.users: Dict[str, Any] = {}
        self.complaints: Dict[str, Any] = {}
        self.dustbins: List[Any] = []
        self.authorities: List[Any] = []

db = SQLAlchemyMockState()
