
<div align="center">
  <img src="https://socialify.git.ci/iamneek/medieo/image?language=1&name=1&pattern=Circuit+Board&theme=Light" alt="medieo"/>
</div>

--- 
**Medieo - Minimal YouTube-like Video Backend (HLS Focus)**

A learning project demonstrating a complete video upload → transcoding → adaptive streaming pipeline using **HLS (HTTP Live Streaming)**.

### Goal
Understand the core concepts of modern video platforms:
- Chunked uploads
- Background processing with Celery
- FFmpeg transcoding to HLS
- Serving video segments via object storage (S3/LocalStack)
- Metadata persistence
- Frontend HLS playback with `hls.js`

---

### Tech Stack

**Backend:**
- FastAPI (Python)
- Celery + Redis (task queue)
- FFmpeg (transcoding)
- boto3 + LocalStack (S3)
- SQLAlchemy + Alembic + NeonDB (PostgreSQL)
- Pydantic

**Frontend:**
- Next.js 15 (App Router)
- TypeScript
- Tailwind + shadcn/ui
- hls.js
- Axios

---

### Architecture Flow

1. **Frontend** → Chunked upload to FastAPI (`/upload/`)
2. **FastAPI** → Saves chunks → assembles video → fires Celery task
3. **Celery Worker** → Runs FFmpeg → generates HLS segments + manifest
4. **FFmpeg** → Outputs `index.m3u8` + `.ts` segments
5. **S3 (LocalStack)** → Stores raw + HLS files
6. **Frontend** → Polls status → gets presigned URL → plays with hls.js

---

### Project Structure (Key Parts)

```
medieo/
├── api/                          # FastAPI backend
│   ├── models/video.py
│   ├── repo/video_repo.py
│   ├── routes/upload_route.py
│   ├── routes/watch_route.py
│   ├── database.py
│   ├── schemas.py
│   └── main.py
├── storage/s3.py
├── tasks/transcoding.py
├── celery_app.py
├── config.py
├── client/                       # Next.js frontend
│   ├── app/
│   │   ├── upload/page.tsx
│   │   ├── watch/[upload_id]/page.tsx
│   │   └── page.tsx (home)
│   └── components/
├── docker-compose.yml (optional)
└── .env
```

---

### Local Setup Guide

#### 1. Prerequisites

- Python 3.11+
- Node.js 20+ + pnpm
- Docker Desktop
- FFmpeg (`winget install ffmpeg` on Windows)
- uv (recommended) or pip

#### 2. Backend Setup

```bash
# Clone / navigate to project
cd medieo

# Create virtual env + install deps
uv venv
uv sync          # or uv pip install -r requirements.txt

# Copy .env template
cp .env.example .env
```

**Edit `.env`:**
```env
REDIS_URL=redis://localhost:6379/0
LOCALSTACK_S3_URL=http://localhost:4566
S3_BUCKET_NAME=medieo
AWS_ACCESS_KEY_ID=test
AWS_SECRET_ACCESS_KEY=test
AWS_REGION=us-east-1
NEON_CONNECTION_STRING=postgresql+psycopg://...
```

#### 3. Start Services (Docker)

```bash
# Redis
docker run -d -p 6379:6379 --name redis redis:alpine

# LocalStack
docker run -d -p 4566:4566 \
  --name localstack \
  -e LOCALSTACK_AUTH_TOKEN=your_token_here \
  localstack/localstack

# Create bucket + CORS
aws --endpoint-url=http://localhost:4566 s3 mb s3://medieo
aws --endpoint-url=http://localhost:4566 s3api put-bucket-cors --bucket medieo --cors-configuration file://cors.json
```

**`cors.json`**:
```json
{
  "CORSRules": [{
    "AllowedOrigins": ["*"],
    "AllowedMethods": ["GET", "HEAD"],
    "AllowedHeaders": ["*"]
  }]
}
```

#### 4. Database Migrations (Alembic)

```bash
cd api
alembic upgrade head
```

#### 5. Run Backend

**Terminal 1** (FastAPI):
```bash
uv run uvicorn api.main:app --reload
```

**Terminal 2** (Celery worker):
```bash
uv run celery -A celery_app worker --pool=solo --loglevel=info
```

---

### Frontend Setup

```bash
cd client
pnpm install
pnpm dev
```

Visit: `http://localhost:3000`

---

NOTE: Localstack used in this manner is not persistent after restart. Therefore, you might need to delete database entries after a restart, or use a real S3 bucket for production.

### How to Use

1. Go to **Upload** page
2. Fill title + description
3. Select video → Upload (chunked)
4. After upload completes → auto-redirects to watch page
5. Video processes in background (watch Celery logs)
6. Once done → HLS video plays via hls.js

---

### Testing the Pipeline

- Small MP4 files recommended for quick testing
- Check LocalStack UI (`http://localhost:4566`) or AWS CLI:
  ```bash
  aws --endpoint-url=http://localhost:4566 s3 ls s3://medieo/videos/ --recursive
  ```

---

### Learning Takeaways

- Why chunked uploads matter (resumability, memory)
- Why background tasks (Celery) are essential for CPU-heavy work
- HLS basics: `.m3u8` manifest + `.ts` segments
- FFmpeg command for HLS (`-f hls -hls_time 10 ...`)
- Object storage + presigned URLs for serving media
- Separation of concerns (API vs Worker vs Storage)
- CORS challenges with S3

---

### Future Improvements (Production Path)

- Multiple quality levels (adaptive bitrate)
- Real CDN (CloudFront)
- Auth + user videos
- Thumbnails + metadata extraction
- Go + asynq version (as originally planned)
- Video validation & virus scanning
- Proper error handling + retries

---

### Commands Cheat Sheet

```bash
# Backend
uv run uvicorn api.main:app --reload
uv run celery -A celery_app worker --pool=solo --loglevel=info

# Frontend
cd client && pnpm dev

# Docker
docker start redis localstack
docker logs localstack -f

# S3
aws --endpoint-url=http://localhost:4566 s3 ls s3://medieo --recursive
```

---

**This project was built as a learning exercise focused on HLS video pipeline concepts.**  
Feel free to extend it or convert the backend to Go for better performance.

Happy learning! 🎥
