# README.md
# AI Video Generator

مشروع MVP عربي كامل لتوليد الفيديوهات بالذكاء الاصطناعي، مبني على:
- Next.js (واجهة المستخدم)
- FastAPI (خدمة API)
- Redis (قائمة الانتظار)
- FFmpeg (تحويل ورسوم الفيديو)
- Docker Compose (تشغيل المشروع محلياً)

## المميزات
- إنشاء فيديو من فكرة نصية
- اختيار نمط الفيديو: سينمائي / أنيمي / واقعي / إعلاني
- تعيين مدة الفيديو
- متابعة حالة المهمة في الوقت الحقيقي
- إنشاء فيديو تجريبي باستخدام FFmpeg
- واجهة عربية جاهزة للتعديل

## البنية
- `frontend/` — واجهة Next.js
- `backend/` — خدمة FastAPI + Worker
- `docker-compose.yml` — تشغيل كامل للحاويات

## التشغيل السريع

### 1) نسخ المتغيرات
```bash
cp .env.example .env
```

### 2) تشغيل المشروع
```bash
docker compose up --build
```

### 3) فتح التطبيق
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/docs

## مثال طلب API
```bash
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "فيديو قصير عن رجل يفتح متجر إلكتروني صغير في المدينة",
    "style": "cinematic",
    "duration": 15,
    "language": "ar"
  }'
```

## متغيرات البيئة
- `NEXT_PUBLIC_API_URL` — عنوان API في الواجهة
- `REDIS_URL` — عنوان Redis

## الملاحظات
هذا المشروع MVP عملي ومهيأ للتوسعة. يمكن ربطه لاحقاً بـ OpenAI / Replicate / Runway / ElevenLabs لتوليد صور وصوت وفيديو حقيقي بدل من الفيديو التجريبي.

## التشغيل يدوي بدون Docker

### Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Worker
```bash
cd backend
source .venv/bin/activate
python worker.py
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```
