# VISIONFORGE - Database Architecture & Schema Specification

**Project Title:** VISIONFORGE - AI Based Intelligent Video Analytics Platform  
**Team Lead:** Jayaprakash R  
**Engine:** PostgreSQL / Supabase (ORM: SQLAlchemy 2.0, Migrations: Alembic)  

---

## 1. Overview & Architectural Principles

The VISIONFORGE database stores video surveillance camera configurations, polygon restricted zones, AI detection outputs, security events, real-time alerts, and runtime system configuration settings.

### Key Principles
1. **No Raw Video Storage in Database:** Video streams and raw frame arrays are processed in worker threads/memory. Only frame metadata, bounding box coordinates, and snapshot file paths are persisted.
2. **Precision & Integrity:** Foreign keys enforce strict referential integrity (`ON DELETE CASCADE` for child zones/events on camera deletion; `ON DELETE SET NULL` for optional references). Check constraints enforce valid bounding box bounds, confidence ranges ($0.0 \le \text{confidence} \le 1.0$), and non-empty strings.
3. **Optimized Indexing:** Common query paths (`timestamp`, `camera_id`, `event_type`, `severity`, `status`, `frame_timestamp`, `object_class`) are indexed for fast filtering and time-series analytics aggregation.
4. **Unified Video Source Architecture:** To prevent redundant schema complexity, video source parameters (`source_type`, `source_url`) are integrated directly into the `cameras` entity rather than maintaining a duplicate `video_sources` table.

---

## 2. Entity Relationship Diagram (ERD)

```
           +----------------------------------+
           |             CAMERAS              |
           +----------------------------------+
           | id (PK, UUID)                    |
           | name (VARCHAR 100)               |
           | location (VARCHAR 200)           |
           | description (VARCHAR 500)        |
           | source_type (ENUM)               |
           | source_url (VARCHAR 500)         |
           | status (ENUM)                    |
           | enabled (BOOLEAN)                |
           | created_at, updated_at           |
           +----------------------------------+
               │ 1                     │ 1
               │                       │
               │ *                     │ *
+-----------------------------+  +-----------------------------+
|            ZONES            |  |         DETECTIONS          |
+-----------------------------+  +-----------------------------+
| id (PK, UUID)               |  | id (PK, UUID)               |
| camera_id (FK -> cameras)   |  | camera_id (FK -> cameras)   |
| name (VARCHAR 100)          |  | event_id (FK -> events, opt)|
| zone_type (ENUM)            |  | object_class (VARCHAR 50)   |
| polygon_coordinates (JSONB) |  | confidence (FLOAT)          |
| enabled (BOOLEAN)           |  | bbox_x, bbox_y (FLOAT)      |
| applicable_object_class     |  | bbox_width, bbox_height     |
| severity (ENUM)             |  | tracking_id (INT, opt)      |
| cooldown_seconds (INT)      |  | frame_timestamp (DATETIME)  |
| created_at, updated_at      |  | metadata (JSONB)            |
+-----------------------------+  +-----------------------------+
               │ 1                             ▲
               │                               │ * (nullable)
               │ * (nullable)                  │
+--------------------------------------------------------------+
|                            EVENTS                            |
+--------------------------------------------------------------+
| id (PK, UUID)                                                |
| event_type (ENUM)                                            |
| camera_id (FK -> cameras.id)                                 |
| zone_id (FK -> zones.id, opt)                                |
| location (VARCHAR 200)                                       |
| timestamp (DATETIME)                                         |
| severity (ENUM)                                              |
| description (VARCHAR 500)                                    |
| detection_data (JSONB)                                       |
| status (ENUM)                                                |
| snapshot_path (VARCHAR 500)                                  |
| created_at, updated_at                                       |
+--------------------------------------------------------------+
               │ 1
               │
               │ *
+--------------------------------------------------------------+
|                            ALERTS                            |
+--------------------------------------------------------------+
| id (PK, UUID)                                                |
| event_id (FK -> events.id)                                   |
| severity (ENUM)                                              |
| title (VARCHAR 150)                                          |
| message (VARCHAR 500)                                        |
| status (ENUM)                                                |
| created_at, updated_at                                       |
| acknowledged_at, resolved_at (DATETIME)                      |
+--------------------------------------------------------------+

+--------------------------------------------------------------+
|                       SYSTEM_SETTINGS                        |
+--------------------------------------------------------------+
| key (PK, VARCHAR 100)                                        |
| value (JSONB)                                                |
| description (VARCHAR 250)                                    |
| updated_at (DATETIME)                                        |
+--------------------------------------------------------------+
```

---

## 3. Database Table Specifications

### 3.1 `cameras`
Stores camera registration, source URLs, and status.
* `id` (UUID, PK)
* `name` (VARCHAR 100, NOT NULL) — Check constraint `length(name) > 0`
* `location` (VARCHAR 200, NULLABLE)
* `description` (VARCHAR 500, NULLABLE)
* `source_type` (ENUM: `LOCAL_VIDEO`, `UPLOAD`, `WEBCAM`, `RTSP`)
* `source_url` (VARCHAR 500, NOT NULL) — Check constraint `length(source_url) > 0`
* `status` (ENUM: `ONLINE`, `OFFLINE`, `CONNECTING`, `ERROR`, `DISABLED`)
* `enabled` (BOOLEAN, DEFAULT `true`)

### 3.2 `zones`
Polygon restricted area monitoring rules.
* `id` (UUID, PK)
* `camera_id` (UUID, FK -> `cameras.id` ON DELETE CASCADE, INDEXED)
* `name` (VARCHAR 100, NOT NULL)
* `zone_type` (ENUM: `RESTRICTED`)
* `polygon_coordinates` (JSONB, NOT NULL) — Array of vertex objects `[{"x": 10, "y": 20}, ...]`
* `enabled` (BOOLEAN, DEFAULT `true`)
* `applicable_object_class` (VARCHAR 50, DEFAULT `'person'`)
* `severity` (ENUM: `LOW`, `MEDIUM`, `HIGH`, `CRITICAL`)
* `cooldown_seconds` (INT, DEFAULT `10`) — Check constraint `cooldown_seconds >= 0`

### 3.3 `events`
Central event registry.
* `id` (UUID, PK)
* `event_type` (ENUM: `PERSON_DETECTED`, `CROWD_DETECTED`, `RESTRICTED_AREA_ENTRY`, `LOITERING`, `UNUSUAL_ACTIVITY`, `CAMERA_OFFLINE`, `CAMERA_RECOVERED`, `SYSTEM_ERROR`)
* `camera_id` (UUID, FK -> `cameras.id` ON DELETE CASCADE, INDEXED)
* `zone_id` (UUID, FK -> `zones.id` ON DELETE SET NULL, NULLABLE)
* `location` (VARCHAR 200, NULLABLE)
* `timestamp` (DATETIME WITH TIME ZONE, NOT NULL, INDEXED)
* `severity` (ENUM: `LOW`, `MEDIUM`, `HIGH`, `CRITICAL`, INDEXED)
* `description` (VARCHAR 500, NULLABLE)
* `detection_data` (JSONB, NULLABLE)
* `status` (ENUM: `NEW`, `ACKNOWLEDGED`, `RESOLVED`, INDEXED)
* `snapshot_path` (VARCHAR 500, NULLABLE)

### 3.4 `detections`
AI object detection frame bounding boxes.
* `id` (UUID, PK)
* `camera_id` (UUID, FK -> `cameras.id` ON DELETE CASCADE, INDEXED)
* `event_id` (UUID, FK -> `events.id` ON DELETE SET NULL, NULLABLE)
* `object_class` (VARCHAR 50, DEFAULT `'person'`, INDEXED)
* `confidence` (FLOAT, NOT NULL) — Check constraint `0.0 <= confidence <= 1.0`
* `bbox_x`, `bbox_y`, `bbox_width`, `bbox_height` (FLOAT, NOT NULL) — Check constraint `width, height >= 0`
* `tracking_id` (INT, NULLABLE)
* `frame_timestamp` (DATETIME WITH TIME ZONE, NOT NULL, INDEXED)
* `metadata` (JSONB, NULLABLE)

### 3.5 `alerts`
Operator actionable notifications.
* `id` (UUID, PK)
* `event_id` (UUID, FK -> `events.id` ON DELETE CASCADE, INDEXED)
* `severity` (ENUM: `LOW`, `MEDIUM`, `HIGH`, `CRITICAL`)
* `title` (VARCHAR 150, NOT NULL)
* `message` (VARCHAR 500, NOT NULL)
* `status` (ENUM: `NEW`, `ACKNOWLEDGED`, `RESOLVED`, INDEXED)
* `acknowledged_at`, `resolved_at` (DATETIME WITH TIME ZONE, NULLABLE)

### 3.6 `system_settings`
Dynamic runtime thresholds.
* `key` (VARCHAR 100, PK) — e.g., `'ai_confidence_threshold'`, `'crowd_threshold'`
* `value` (JSONB, NOT NULL)
* `description` (VARCHAR 250, NULLABLE)

---

## 4. Migration Guide (Alembic)

### Configuration
Alembic migrations are configured in `alembic.ini` and `backend/alembic/env.py`. Database credentials are loaded dynamically from `backend.app.core.config.settings.DATABASE_URL`.

### Commands

**Generate Static SQL Migration Script (Offline Mode):**
```powershell
$env:PYTHONPATH="."; .\backend\.venv\Scripts\python.exe -m alembic upgrade head --sql
```

**Apply Migrations to Live PostgreSQL Instance:**
```powershell
$env:PYTHONPATH="."; .\backend\.venv\Scripts\python.exe -m alembic upgrade head
```

**Roll Back Last Migration:**
```powershell
$env:PYTHONPATH="."; .\backend\.venv\Scripts\python.exe -m alembic downgrade -1
```
