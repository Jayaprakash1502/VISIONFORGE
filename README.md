# VISIONFORGE — AI Based Intelligent Video Analytics Platform

> **"We are not building another CCTV system. We are making existing surveillance systems intelligent."**

VISIONFORGE is an AI-powered surveillance monitoring platform that transforms existing CCTV/video feeds into intelligent automated monitoring systems. It analyzes live or recorded video streams, detects persons using Ultralytics YOLOv8, tracks people count, evaluates polygonal restricted-area entry breaches, monitors crowd thresholds and loitering, and generates real-time dashboard alerts for human security operators.

---

## 🚀 Key Features (Version 1 Scope)

- **Live & Recorded Video Processing:** Stream processing powered by OpenCV.
- **YOLOv8 Person Detection:** Real-time person bounding box extraction, confidence scores, and centroids.
- **Real-Time People Counting:** Live count aggregation updated dynamically on every frame.
- **Polygon Restricted-Area Detection:** Interactive polygonal zone monitoring (Restricted Zone A) with centroid intersection logic.
- **Crowd Threshold Analysis:** Configurable crowd density monitoring (`CROWD_DETECTED` events when count $\ge 5$).
- **Loitering Detection:** Temporal state tracking for persons remaining inside monitored regions past threshold limits ($>15\text{s}$).
- **Centralized Event & Alert Engines:** Cooldown debouncing to prevent event flooding, severity mapping (`LOW`, `MEDIUM`, `HIGH`, `CRITICAL`), and operator lifecycle states (`NEW`, `ACKNOWLEDGED`, `RESOLVED`).
- **Human-in-the-Loop Operator Dashboard:** Dark Security Operations Center (SOC) UI with live canvas streaming, active alert panels, event audit history, and Recharts analytics.

---

## 🛠️ Technology Stack

- **Frontend:** React 18, TypeScript, Vite, Tailwind CSS, Recharts, Lucide React icons.
- **Backend:** Python 3.11, FastAPI, Pydantic v2, SQLAlchemy 2.0 ORM, Alembic migrations, Uvicorn.
- **Computer Vision & AI:** OpenCV (`opencv-python`), Ultralytics YOLO (`yolov8n.pt`), Shapely, NumPy.
- **Real-Time Communication:** WebSockets (`/ws/events`), MJPEG stream (`/api/video/stream`), polling API fallback.

---

## 📁 Repository Structure

```
VISIONIQ/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app factory, CORS, exception handlers
│   │   ├── core/                # Config, logging with secret masking, database, store, websocket
│   │   ├── models/              # SQLAlchemy 2.0 ORM domain schemas (Camera, Zone, Event, Alert, etc.)
│   │   ├── schemas/             # Pydantic v2 validation schemas
│   │   ├── ai/                  # YOLOv8 object detector service
│   │   ├── video/               # OpenCV frame capture and rule processing engine
│   │   └── api/v1/              # FastAPI REST routers (/cameras, /events, /alerts, /video, /health)
│   ├── tests/                   # Pytest test suite (17/17 passing tests)
│   └── requirements.txt         # Pinned Python backend dependencies
├── frontend/
│   ├── src/
│   │   ├── components/          # Navbar, KPICards, VideoPlayer, AlertsPanel, EventDetailModal
│   │   ├── pages/               # Dashboard, LiveMonitoring, Cameras, Events, Alerts, Analytics, Settings
│   │   ├── services/            # Axios API client
│   │   ├── App.tsx              # Main React application
│   │   └── main.tsx             # Entry point
│   ├── package.json
│   └── vite.config.ts
├── data/
│   ├── create_demo_video.py     # Synthetic surveillance demo video generator
│   └── videos/demo.mp4          # Demo video clip
├── docs/
│   ├── DEMO_GUIDE.md            # Step-by-step Review 1 demonstration walkthrough
│   ├── DATABASE.md              # Database ERD & table specifications
│   └── IMPLEMENTATION_PLAN.md   # Architectural specifications & phase roadmap
├── AGENTS.md                    # Permanent engineering & compliance rules
├── alembic.ini                  # Alembic migration configuration
└── README.md
```

---

## ⚙️ Quick Start Instructions

### 1. Prerequisites
- Python 3.11+
- Node.js v24+ & npm

### 2. Backend Startup
Open Terminal 1:
```powershell
$env:PYTHONPATH="."
.\backend\.venv\Scripts\python.exe -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```
*Backend API server runs at: `http://127.0.0.1:8000`*  
*Swagger Documentation: `http://127.0.0.1:8000/docs`*

### 3. Frontend Startup
Open Terminal 2:
```powershell
cd frontend
cmd /c "npm run dev"
```
*Frontend SOC Dashboard runs at: `http://localhost:5173`*

---

## 🧪 Running Automated Tests

Run the backend test suite (17 unit & integration tests covering config, health, models, schemas, exceptions, database fallback, and CORS):
```powershell
$env:PYTHONPATH="."
.\backend\.venv\Scripts\python.exe -m pytest backend/tests -v
```

---

## 🎯 Review 1 Demo Checklist

1. Open `http://localhost:5173`.
2. Click **START ANALYSIS** on the main dashboard.
3. Observe live person bounding boxes (`Person 88%`), centroid points, and live count.
4. Watch person enter **Restricted Zone A** — zone highlights bright RED, triggering `RESTRICTED_AREA_ENTRY` event and **HIGH** severity alert.
5. Click **Acknowledge** and **Resolve Alert** on the right panel.
6. View event audit history under **Events** tab.

---

## 📋 Scope Boundaries (Future Scope)

The following features belong to future phases and are excluded from Version 1:
- Face Recognition & ANPR / License Plate Recognition.
- Vehicle Detection & Fire / Smoke Detection.
- Fall Detection & Violence / Fight Detection.
- Multi-camera Re-ID & Predictive Analytics.
