from pydantic import BaseModel, Field
from typing import Literal, Optional


class VideoRequest(BaseModel):
    prompt: str = Field(..., min_length=5, max_length=1000)
    style: Literal["cinematic", "realistic", "anime", "commercial"] = "cinematic"
    duration: int = Field(default=15, ge=5, le=90)
    language: str = Field(default="ar")


class VideoJobResponse(BaseModel):
    job_id: str
    status: str = "queued"
    message: str


class VideoJob(BaseModel):
    job_id: str
    prompt: str
    style: str
    duration: int
    language: str
    status: str = "queued"
    output_url: Optional[str] = None
    created_at: str
    updated_at: str
