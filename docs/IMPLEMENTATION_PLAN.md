# VISIONFORGE - Architectural Specification & Comprehensive Implementation Plan

**Project Title:** VISIONFORGE - AI Based Intelligent Video Analytics Platform  
**Team Lead:** Jayaprakash R  
**Team Members:** Jayaprakash R, Harisudhan S, Ezhilarasi K  
**Core Mission:** *"We are not building another CCTV system. We are making existing surveillance systems intelligent."*  

---

## 1. Current Repository & Environment Analysis

### Initial Workspace Audit
- **Repository State:** Clean workspace (`c:\Users\Jayaprakash\OneDrive\Desktop\VISIONIQ`) ready for initialization.
- **Node.js Environment:** Node.js `v24.21.0` with `npm` `11.19.0` available.
- **Python Environment:** Python `3.11.9` available.
- **Computer Vision & AI Dependencies:** `opencv-python` and `ultralytics` (YOLOv8) to be installed in a dedicated Python virtual environment (`venv`).
- **Database System:** PostgreSQL / Supabase target architecture with SQLAlchemy ORM + Alembic migrations (fallback to local PostgreSQL / SQLite for isolated testing).
- **Execution Environment:** Windows x64 CPU host. AI pipeline optimized via frame sampling (configurable 5–10 inference FPS vs 30 capture FPS) and frame resizing.

---

## 2. Overall System Architecture

VISIONFORGE employs a decoupled, multi-tier modular architecture designed for real-time video processing, low latency, and operational stability.

```
+-----------------------------------------------------------------------------------+
|                                   VIDEO SOURCES                                   |
|               Local MP4 File  |  Uploaded Video  |  RTSP Stream  |  Webcam        |
+-----------------------------------------------------------------------------------+
                                         │
                                         ▼
+-----------------------------------------------------------------------------------+
|                               VIDEO CAPTURE SERVICE                               |
|                  OpenCV VideoCapture Thread Pool / Bounded Queue                  |
+-----------------------------------------------------------------------------------+
                                         │ (Sampled Frames: e.g. 5-10 FPS)
                                         ▼
+-----------------------------------------------------------------------------------+
|                                FRAME PROCESSOR & AI                               |
|                 YOLOv8 Engine (Person Detection + Bounding Boxes)                |
+-----------------------------------------------------------------------------------+
                                         │ (Detections + Coordinates)
                                         ▼
+-----------------------------------------------------------------------------------+
|                            TEMPORAL & RULE ANALYSIS                               |
|  • People Counting & Crowd Thresholds  • Polygon Restricted Zone Intersections   |
|  • Loitering State Tracking & Timers   • Predefined Movement / Activity Rules     |
+-----------------------------------------------------------------------------------+
                                         │ (State Breaches / Events)
                                         ▼
+-----------------------------------------------------------------------------------+
|                               EVENT & ALERT SERVICE                               |
|      Event Engine (Cooldown / Debouncing) ──► Alert Engine (Severity Mapping)     |
+-----------------------------------------------------------------------------------+
                                   │                      │
                                   ▼                      ▼
                     +---------------------------+   +----------------------------+
                     |    POSTGRESQL DATABASE    |   |     WEBSOCKET MANAGER      |
                     | (Events, Alerts, Cameras) |   | (Real-time Broadcast push) |
                     +---------------------------+   +----------------------------+
                                                          │
                                                          ▼
                                             +----------------------------+
                                             |     REACT / VITE DASHBOARD |
                                             |  (Live Canvas, SOC UI)     |
                                             +----------------------------+
```

---

## 3. Frontend Architecture

- **Framework:** React 18 + TypeScript + Vite
- **Styling:** Tailwind CSS (Dark-themed Security Operations Center palette: Slate/Zinc dark backgrounds, Cyan/Blue AI accents, Emerald status indicators, Amber loitering warnings, Red critical alerts).
- **Icons:** Lucide React (`lucide-react`)
- **Visualizations & Charts:** Recharts
- **State & Real-Time Management:** React Hooks, Context API, Native WebSocket with automatic backoff reconnection logic.
- **Canvas Rendering:** Dynamic HTML5 Canvas overlaid on video streams to render bounding boxes, polygon zones, counts, and active alert overlays smoothly at display FPS.

### Component Structure
```
frontend/src/
├── assets/
├── components/
│   ├── common/           # Button, Modal, Badge, Card, Spinner, Navbar, Sidebar
│   ├── dashboard/        # KPICard, AlertWidget, CameraGridWidget, EventTimelineWidget
│   ├── monitoring/       # VideoCanvasPlayer, ZoneDrawer, MultiCameraGrid, StreamControls
│   ├── cameras/          # CameraFormModal, CameraCard, CameraStatusBadge
│   ├── events/           # EventTable, EventFilterBar, EventDetailModal
│   ├── alerts/           # AlertBanner, AlertList, ActionButtons
│   └── analytics/        # EventsChart, PeopleCountChart, ZoneBreachDistribution
├── pages/
│   ├── DashboardPage.tsx
│   ├── LiveMonitoringPage.tsx
│   ├── CamerasPage.tsx
│   ├── EventsPage.tsx
│   ├── AlertsPage.tsx
│   ├── AnalyticsPage.tsx
│   └── SettingsPage.tsx
├── services/
│   ├── api.ts            # Axios / Fetch client wrapper
│   ├── websocket.ts      # Resilient WebSocket connection manager
│   └── cameraService.ts
├── hooks/
│   ├── useWebSocket.ts
│   ├── useCameras.ts
│   └── useEvents.ts
└── types/
    ├── index.ts          # Camera, Zone, Detection, Event, Alert TypeScript interfaces
```

---

## 4. Backend Architecture

- **Framework:** Python 3.11 + FastAPI + Pydantic v2
- **ORM & DB Access:** SQLAlchemy 2.0 async / sync engine with PostgreSQL backend
- **Concurrency Model:** Asyncio event loop for HTTP API & WebSockets; isolated background thread worker processes for OpenCV video ingest and YOLO AI inference.
- **Process Isolation:** OpenCV capture loops run in dedicated worker threads with bounded FIFO queues. If a stream disconnects or fails, the worker catches the error, sets camera status to `OFFLINE` or `ERROR`, and retries without affecting FastAPI API endpoints or other camera threads.

---

## 5. AI Computer Vision Pipeline

```
Raw Frame -> Rescale/Resize (640x360) -> Inference Frame Skip (e.g. process 1 in 3 frames)
  -> YOLOv8 Model Inference -> Filter Class 'person' (ID: 0) -> Confidence Filter (e.g. >0.45)
  -> Bounding Box (x1, y1, x2, y2) + Centroid Calculation (cx, cy)
  -> Polygon Intersection Testing (Shapely / OpenCV pointPolygonTest)
  -> Temporal Tracking & Loitering Timer Evaluation
  -> Rule Engine & Cooldown Checker -> Event Triggering
```

1. **Model Management:** Modular `ModelManager` loading `yolov8n.pt` / `yolov8s.pt` with automatic CPU/CUDA detection. Graceful startup check: if weights are missing, prompt setup commands cleanly without crashing server.
2. **Detection Service:** Extracts person bounding boxes, confidence scores, centroids, and frame timestamps.
3. **Polygon Zone Verification:** Ray-casting / OpenCV `pointPolygonTest` checks if person centroid `(cx, cy)` or bounding box bottom-center `(cx, y2)` resides inside user-defined multi-vertex zones.
4. **Loitering Detection:** Maintains object ID state across consecutive frames using centroid tracking. If an object remains inside a zone past `loitering_threshold_seconds`, trigger `LOITERING` event.
5. **Debouncing / Cooldown:** Event engine enforces configurable cooldown timers per zone/rule to prevent event flooding (e.g. 10-second cooldown before duplicate alert for same zone).

---

## 6. Database Schema Design (PostgreSQL / Supabase)

### Relational Schema Diagram Overview

```
 +--------------------+       +--------------------+       +--------------------+
 |      CAMERAS       |       |       ZONES        |       |     DETECTIONS     |
 +--------------------+       +--------------------+       +--------------------+
 | id (PK, UUID)      |1    * | id (PK, UUID)      |       | id (PK, UUID)      |
 | name               |◄──────| camera_id (FK)     |       | camera_id (FK)     |
 | location           |       | name               |       | timestamp          |
 | source_type        |       | polygon_coords     |       | person_count       |
 | source_url         |       | enabled            |       | bounding_boxes     |
 | status             |       | severity           |       +--------------------+
 | created_at         |       +--------------------+
 +--------------------+
           │ 1
           │
           │ *
 +--------------------+       +--------------------+       +--------------------+
 |       EVENTS       |1    1 |       ALERTS       |       |  SYSTEM_SETTINGS   |
 +--------------------+       +--------------------+       +--------------------+
 | id (PK, UUID)      |◄──────| id (PK, UUID)      |       | key (PK, Text)     |
 | event_type         |       | event_id (FK)      |       | value (JSONB)      |
 | camera_id (FK)     |       | severity           |       | description        |
 | zone_id (FK, opt)  |       | status             |       | updated_at         |
 | timestamp          |       | acknowledged_by    |       +--------------------+
 | severity           |       | resolved_at        |
 | description        |       +--------------------+
 | detection_data     |
 | snapshot_path      |
 +--------------------+
```

### Table Specifications & Indexes
- **cameras:** Stores camera configuration, stream source URLs, and connection status (`ONLINE`, `OFFLINE`, `CONNECTING`, `ERROR`, `DISABLED`).
- **zones:** Polygon vertices JSON (`[[x1,y1], [x2,y2], ...]`), rule definitions, and severity levels linked to cameras.
- **events:** Logged security events (`PERSON_DETECTED`, `CROWD_DETECTED`, `RESTRICTED_AREA_ENTRY`, `LOITERING`, `UNUSUAL_ACTIVITY`, `CAMERA_OFFLINE`). Indexing on `(created_at DESC)`, `camera_id`, `event_type`, `severity`.
- **alerts:** Actionable operator notifications linked to events with lifecycle statuses (`NEW`, `ACKNOWLEDGED`, `RESOLVED`).
- **system_settings:** Configurable thresholds (`confidence_threshold`, `inference_fps`, `crowd_threshold`, `loitering_threshold_seconds`, `cooldown_seconds`).

---

## 7. API Specification (FastAPI REST)

| Category | Endpoint | Method | Description |
|---|---|---|---|
| **Health** | `/api/v1/health` | GET | Operational health check & model readiness status |
| **Auth** | `/api/v1/auth/login` | POST | Authenticates user & issues JWT token |
| | `/api/v1/auth/me` | GET | Returns current user details |
| **Cameras** | `/api/v1/cameras` | GET/POST | List all cameras / Register new camera source |
| | `/api/v1/cameras/{id}` | GET/PUT/DELETE | Get details, update stream URL, or remove camera |
| | `/api/v1/cameras/{id}/start` | POST | Start background video capture & AI stream |
| | `/api/v1/cameras/{id}/stop` | POST | Stop active capture worker thread |
| **Zones** | `/api/v1/cameras/{id}/zones` | GET/POST | Retrieve or add polygon restricted zones |
| | `/api/v1/zones/{id}` | PUT/DELETE | Update zone polygon coordinates or delete zone |
| **Events** | `/api/v1/events` | GET | Filterable event history with pagination |
| | `/api/v1/events/{id}` | GET/PATCH | Get event details or update status |
| **Alerts** | `/api/v1/alerts` | GET | Fetch active/unacknowledged alerts |
| | `/api/v1/alerts/{id}/acknowledge` | PATCH | Mark alert as acknowledged by operator |
| | `/api/v1/alerts/{id}/resolve` | PATCH | Mark alert as resolved |
| **Analytics** | `/api/v1/analytics/summary` | GET | KPI metrics (Active cameras, Total events, Crowd alerts) |
| | `/api/v1/analytics/timeline` | GET | Time-series count of events & people count trends |
| **Settings** | `/api/v1/settings` | GET/PUT | Read and update system AI thresholds |

---

## 8. Real-Time WebSocket Interface

- **Endpoint:** `/ws/events`
- **Protocol:** JSON over WebSocket with keep-alive heartbeat ping/pong.
- **Message Payloads:**
  - `event.created`: Published immediately when an event occurs.
  - `alert.created`: Published when a HIGH or CRITICAL alert is triggered.
  - `camera.status`: Broadcasts status updates (`ONLINE`, `OFFLINE`, `ERROR`).
  - `detection.updated`: Streamed live frame metrics (Current Person Count, Bounding Box coordinates, Frame Timestamp).

---

## 9. Planned Folder Structure

```
VISIONIQ/
├── AGENTS.md
├── README.md
├── docker-compose.yml
├── .env.example
├── .gitignore
├── docs/
│   ├── IMPLEMENTATION_PLAN.md
│   ├── ARCHITECTURE.md
│   ├── AI_PIPELINE.md
│   ├── DATABASE.md
│   ├── API.md
│   ├── TESTING.md
│   ├── SECURITY.md
│   └── FUTURE_SCOPE.md
├── data/
│   ├── videos/             # Local demo videos (demo.mp4)
│   ├── evidence/           # Event snapshot images
│   └── models/             # YOLO weights (yolov8n.pt)
├── backend/
│   ├── requirements.txt
│   ├── pyproject.toml
│   └── app/
│       ├── main.py
│       ├── core/           # Config, logging, security, database.py
│       ├── models/         # SQLAlchemy ORM schemas
│       ├── schemas/        # Pydantic schemas
│       ├── api/            # FastAPI routes (v1 endpoints)
│       ├── ai/             # YOLO engine, polygon math, temporal tracking
│       ├── video/          # OpenCV stream capture, demo video player thread
│       ├── events/         # Rule engine, alert dispatcher, debouncer
│       └── workers/        # Camera stream worker threads & background tasks
├── frontend/
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   ├── tsconfig.json
│   └── src/
└── tests/
    ├── backend/            # Pytest suite (API, AI pipeline, rules)
    └── frontend/           # Component & integration tests
```

---

## 10. Phase-by-Phase Implementation Roadmap

- **Phase 1: Inspection & Architecture (Current Phase)**  
  Perform environment audit, establish guidelines in `AGENTS.md`, and write `docs/IMPLEMENTATION_PLAN.md`. Obtain Team Lead approval.
- **Phase 2: Backend Foundation**  
  Set up Python virtual environment, FastAPI project structure, Pydantic settings, logging, and `/api/v1/health` endpoint.
- **Phase 3: Database & Models**  
  Configure SQLAlchemy database models (Cameras, Zones, Detections, Events, Alerts, SystemSettings), DB engine initialization, and initial migrations.
- **Phase 4: Video Capture Engine & Demo Mode**  
  Implement OpenCV video stream reader with thread isolation, sample frame generation, and local recorded video (`data/videos/demo.mp4`) demo runner.
- **Phase 5: YOLO AI Detection Service**  
  Integrate Ultralytics YOLOv8 for person class detection, bounding box extraction, confidence filtering, and non-blocking inference.
- **Phase 6: People Counting & Crowd Analysis Engine**  
  Build real-time counting aggregation and configurable crowd threshold analysis (`NORMAL`, `CROWDED`, `HIGH CROWD`).
- **Phase 7: Polygon Restricted Area Detection**  
  Implement interactive polygon zone checking using vector geometry / OpenCV `pointPolygonTest` to detect zone entry.
- **Phase 8: Temporal Analysis & Loitering Rules**  
  Build temporal state tracking for loitering detection (`loitering_threshold_seconds`) and debouncing/cooldown logic.
- **Phase 9 & 10: Event & Alert Engines**  
  Implement central event lifecycle and alert dispatching with severity levels (`LOW`, `MEDIUM`, `HIGH`, `CRITICAL`).
- **Phase 11: Real-Time WebSocket Infrastructure**  
  Build FastAPI WebSocket manager to broadcast `event.created`, `alert.created`, and live detection overlays to connected clients.
- **Phase 12: Frontend Shell & SOC UI System**  
  Initialize Vite + React + TypeScript + Tailwind CSS application with security center layout, sidebar, dark theme, and navigation.
- **Phase 13: Live Monitoring & Camera Command Center**  
  Build canvas player component for live bounding box rendering, interactive polygon zone drawer, and camera management UI.
- **Phase 14: Event History, Alert Center & Analytics**  
  Implement searchable/filterable event history table, alert action modal (Acknowledge/Resolve), and Recharts visual analytics dashboard.
- **Phase 15: Integration Testing & Hardening**  
  Run end-to-end tests across the full video -> AI -> event -> alert -> UI pipeline.
- **Phase 16: Documentation, Docker & Final Verification**  
  Finalize comprehensive README, technical docs in `docs/`, Docker setup, and final verification report.

---

## 11. Testing & QA Strategy

1. **Backend Tests (`pytest`):**
   - Health check & API route status codes.
   - Camera CRUD operations & validation.
   - Geometry math tests (polygon containment, bounding box centroid math).
   - Temporal tracking & loitering timer logic unit tests.
   - Cooldown debouncer test.
2. **Integration Test (End-to-End Core Verification):**
   - Input demo video stream.
   - Run OpenCV + YOLO person detection.
   - Simulate person entering defined polygon restricted zone.
   - Verify `RESTRICTED_AREA_ENTRY` event creation.
   - Verify matching `HIGH` severity alert creation.
   - Verify WebSocket payload emission.
   - Acknowledge alert via API and verify status changes to `ACKNOWLEDGED`.
3. **Frontend Tests:**
   - Type-checking with TypeScript (`tsc --noEmit`).
   - Vite production build verification (`npm run build`).

---

## 12. Security Strategy

- **Authentication & Authorization:** Secure JWT bearer token authentication for protected API endpoints.
- **Secret Management:** Strict isolation of database strings, JWT secret keys, and stream credentials in environment variables (`.env`).
- **Input Sanitization:** Validate all polygon coordinate arrays, camera URL inputs, and numeric thresholds with Pydantic.
- **CORS Configuration:** Explicitly restrict CORS origins in FastAPI to approved frontend origins.
- **Safe Logging:** Guarantee that sensitive fields (passwords, tokens, RTSP credentials) are masked before write to stdout/log files.

---

## 13. Performance & Optimization Strategy

- **Frame Sampling:** Inference runs on a subset of frames (e.g. 5–10 FPS out of 30 FPS video input) to minimize CPU usage while keeping visual output smooth.
- **Image Resizing:** Input frames are downscaled (e.g., 640x360 or 640x480) before passing into YOLO engine.
- **Bounded Queues:** Capture threads feed frames into thread-safe bounded queues (`maxsize=2`), dropping stale frames if inference falls behind.
- **Canvas Rendering:** Frontend uses HTML5 `<canvas>` hardware acceleration for smooth 60 FPS rendering of bounding boxes and polygonal zones over video elements.

---

## 14. Demo Strategy & Hardware Fallback

- **Reliable Local Video Demo Mode:** To ensure 100% dependable demonstration without external RTSP hardware or live cameras, a dedicated sample video file (`data/videos/demo.mp4`) will be provided in the repository.
- **Full AI Real-Time Execution:** Demo mode passes local video frames through the **exact real OpenCV -> YOLO -> Rule Engine -> Event Engine -> WebSocket -> React Dashboard** pipeline. Zero fake detections or hardcoded states.

---

## 15. Risk Assessment & Mitigation Matrix

| Identified Risk | Impact | Mitigation Strategy |
|---|---|---|
| **CPU Performance Bottleneck during YOLO inference** | Medium | Implement frame sampling (process 1 out of 3/5 frames), downscale inference dimensions (640px), and use lightweight model `yolov8n.pt`. |
| **Video stream disconnect / invalid RTSP URL** | High | Wrap OpenCV stream reading in dedicated worker threads with automatic status update to `OFFLINE` and reconnect retries. Prevent main API process from crashing. |
| **High volume of duplicate alerts for loitering person** | Medium | Implement strict event debouncing & cooldown timers per camera/zone tuple. |
| **PowerShell script execution restriction on Windows (`npm.ps1`)** | Low | Execute npm commands via `cmd /c npm ...` or standard command runner. |

---

## 16. Core Dependencies & Libraries

### Backend Python Packages
- `fastapi` & `uvicorn` (Async web framework & server)
- `pydantic` & `pydantic-settings` (Data validation & environment config)
- `sqlalchemy` & `alembic` (ORM & database migrations)
- `opencv-python` (Frame extraction, image processing, geometry)
- `ultralytics` (YOLOv8 object detection)
- `shapely` (Polygon intersection & geometric calculations)
- `python-jose` & `passlib` (JWT authentication & password hashing)
- `pytest` & `httpx` (Automated testing)

### Frontend Node Packages
- `react` & `react-dom` (UI library)
- `typescript` (Static typing)
- `vite` (Bundler & dev server)
- `tailwindcss` & `autoprefixer` (Utility-first styling)
- `recharts` (Data visualization charts)
- `lucide-react` (Iconography)
- `axios` (HTTP client)
