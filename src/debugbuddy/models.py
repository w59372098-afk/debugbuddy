from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class DebugReport:
    error_type: str
    message: str
    explanation: str
    likely_cause: str
    suggestions: List[str] = field(default_factory=list)
    file_path: Optional[str] = None
    line_number: Optional[int] = None
    source_line: Optional[str] = None
    context: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "error_type": self.error_type,
            "message": self.message,
            "explanation": self.explanation,
            "likely_cause": self.likely_cause,
            "suggestions": self.suggestions,
            "file_path": self.file_path,
            "line_number": self.line_number,
            "source_line": self.source_line,
            "context": self.context,
        }
