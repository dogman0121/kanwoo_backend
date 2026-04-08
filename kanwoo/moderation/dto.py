from dataclasses import dataclass
from typing import Optional

@dataclass
class ModerationStatusUpdateDTO:
    status_type_id: int
    message: Optional[str]