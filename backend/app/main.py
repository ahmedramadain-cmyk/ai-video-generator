import json
import os
import uuid
from datetime import datetime, timezone
from typing import Dict, List

import redis
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.schemas import VideoJob, VideoJobRequest, VideoJobResponse

settings = get_settings()
app = FastAPI(title=settings.app_title)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

r = redis.Redis.from_url(settings.redis_url, decode_responses=True)
JOBS: Dict[str, VideoJob] = {}


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "backend"}


@app.post("/api/generate", response_model=VideoJobResponse)
def create_job(request: VideoJobRequest):
    job_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    job = VideoJob(
        job_id=job_id,
        prompt=request.prompt,
        style=request.style,
        duration=request.duration,
        language=request.language,
        status="queued",
        created_at=now,
        updated_at=now,
    )
    JOBS[job_id] = job
    payload = {
        "job_id": job_id,
        "prompt": request.prompt,
        "style": request.style,
        "duration": request.duration,
        "language": request.language,
    }
    r.lpush("video_jobs", json.dumps(payload))
    return VideoJobResponse(job_id=job_id, status="queued", message="تمت إضافة المهمة إلى قائمة الانتظار")


@app.get("/api/jobs")
def list_jobs():
    return {"jobs": [job.model_dump() for job in JOBS.values()]}


@app.get("/api/jobs/{job_id}")
def get_job(job_id: str):
    job = JOBS.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="job not found")
    return job.model_dump()


@app.get("/")
def root():
    return {"message": "AI Video Generator API"}
