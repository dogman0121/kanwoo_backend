from dataclasses import dataclass

@dataclass
class ReportCreateDTO:
    type_id: int
    comment: str