from pydantic import BaseModel, Field
from typing import Optional, List

class SymptomResponse(BaseModel):
    probable_cause: str = Field(
        ..., description="What could be causing this symptom"
    )
    severity: str = Field(
        ..., description="Severity level: mild / moderate / severe"
    )
    advice: str = Field(
        ..., description="Advice for next steps"
    )
    log_status: str = Field(
        default="", description="Status of logging"
    )
    audio_response: Optional[str] = Field(
        default=None, description="Audio response file path"
    )

class ChatRequest(BaseModel):
    message: str = Field(..., description="User message")
    session_id: str = Field(default="default", description="Session ID")
    files: Optional[List[str]] = Field(default=None, description="Uploaded file paths")
    audio_input: Optional[str] = Field(default=None, description="Audio input file path")
