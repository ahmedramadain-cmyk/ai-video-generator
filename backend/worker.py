import json
import os
import subprocess
import time
from datetime import datetime, timezone

import redis

from app.config import get_settings
from app.schemas import VideoJob

settings = get_settings()
r = redis.Redis.from_url(settings.redis_url, decode_responses=True)

JOBS = {}


def update_job(job_id: str, **kwargs):
    job = JOBS.get(job_id)
    if job is None:
        return
    for key, value in kwargs.items():
        setattr(job, key, value)
    job.updated_at = datetime.now(timezone.utc).isoformat()


def ensure_output_dir():
    os.makedirs("/tmp/ai-video-output", exist_ok=True)


def build_video_file(job_id: str, prompt: str, duration: int, style: str):
    ensure_output_dir()
    output_path = f"/tmp/ai-video-output/{job_id}.mp4"
    subtitle = prompt[:80].replace("'", "")
    cmd = [
        "ffmpeg",
        "-y",
        "-f",
        "lavfi",
        "-i",
        f"color=c=0x0b1020:s=1280x720:d={duration}",
        "-vf",
        f"drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:text='{subtitle}':fontcolor=white:fontsize=32:x=(w-text_w)/2:y=h-th-40:shadowcolor=black:shadowx=2:shadowy=2",
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        output_path,
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return output_path


def process_job(payload: dict):
    job_id = payload["job_id"]
    if job_id not in JOBS:
        JOBS[job_id] = VideoJob(
            job_id=job_id,
            prompt=payload["prompt"],
            style=payload["style"],
            duration=payload["duration"],
            language=payload["language"],
            status="queued",
            created_at=datetime.now(timezone.utc).isoformat(),
            updated_at=datetime.now(timezone.utc).isoformat(),
        )

    job = JOBS[job_id]
    update_job(job_id, status="processing")
    time.sleep(1)

    try:
        output_file = build_video_file(job_id, payload["prompt"], payload["duration"], payload["style"])
        update_job(job_id, status="completed", output_url=output_file)
    except Exception as exc:
        update_job(job_id, status="failed")
        print(f"Job failed: {exc}")


def main():
    while True:
        item = r.rpop("video_jobs")
        if item is None:
            time.sleep(1)
            continue
        payload = json.loads(item)
        process_job(payload)


if __name__ == "__main__":
    main()
