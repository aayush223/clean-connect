from datetime import datetime, timedelta
from typing import Dict

class SLAManager:
    """Enforces, updates, and monitors the strict 36-hour resolution timeline."""
    @staticmethod
    def calculate_sla_window() -> Dict[str, datetime]:
        now = datetime.now()
        deadline = now + timedelta(hours=36)
        return {
            "created_at": now,
            "deadline_at": deadline
        }

    @staticmethod
    def check_sla_compliance(deadline_at: datetime) -> bool:
        return datetime.now() <= deadline_at
