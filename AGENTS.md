# AGENTS.md - VISIONFORGE Operating Guidelines & Rules

## Project Identity
- **Project Name:** VISIONFORGE (AI Based Intelligent Video Analytics Platform)
- **Team Lead:** Jayaprakash R
- **Team Members:** Jayaprakash R, Harisudhan S, Ezhilarasi K
- **Core Mission:** "We are not building another CCTV system. We are making existing surveillance systems intelligent."

---

## 1. Fundamental Engineering Rules

### Codebase & Architecture Principles
1. **Inspect Before Modifying:** Always inspect existing repository files, structure, and configurations before adding or modifying code.
2. **Preserve Working Functionality:** Retain and build upon valid existing functionality. Never blindly overwrite working code.
3. **Avoid Duplication:** Prevent duplicate table definitions, duplicate API endpoints, duplicate utility functions, or parallel microservices.
4. **Strict Modular Isolation:** Keep video capture, OpenCV frame processing, YOLO AI inference, temporal analysis, event logic, alert handling, database persistence, and WebSocket broadcasting strictly separated into modular packages.
5. **No Main Loop Blocking:** Never place blocking AI inference or video streaming loops inside FastAPI request handlers or main event loop threads. Use isolated worker threads/processes.
6. **Error Isolation:** A camera capture error or worker failure must never crash the backend API server or affect other active cameras.

---

## 2. Integrity & Quality Guidelines

### AI & Data Integrity
1. **Never Fake AI Results:** Never hardcode fake detections, synthetic statistics, or mock alerts to simulate functionality. All detections, counts, loitering states, and restricted-area breaches must be computed by the real computer vision & rule engine pipeline.
2. **Clear Demo & Simulation Labeling:** If local test samples or dry-run scripts are used for testing without live streams, process real recorded video files through the full AI pipeline. UI simulations for disconnected hardware testing must be clearly labeled as `SIMULATION MODE`.

### Security & Data Protection
1. **Never Expose Secrets:** Never hardcode RTSP credentials, passwords, database URIs, API keys, or JWT secrets in code or commits.
2. **Environment Configuration:** Always use `.env` files and environment variables. Provide `.env.example` with standard placeholders.
3. **Input Validation:** Strictly validate all incoming HTTP payloads, WebSocket parameters, polygon coordinates, threshold values, and camera URLs using Pydantic / TypeScript schemas.
4. **Safe Database Operations:** Use parameterized ORM queries (SQLAlchemy) to prevent SQL injection.
5. **Safe Logging:** Never log passwords, tokens, API keys, database credentials, or RTSP authentication strings.

---

## 3. Scope & Extensibility

### Scope Boundary Control
1. **Strict Version 1 Scope:** Focus exclusively on Person Detection, People Counting, Crowd Analysis, Polygon Restricted-Area Entry, Loitering Detection, Predefined Unusual Activity Rules, Dashboard Alerts, Live Monitoring, Camera Management, Event History, and Analytics.
2. **De-prioritized Future Scope:** Do NOT implement Face Recognition, ANPR/License Plate Recognition, Vehicle Detection, Fire/Smoke Detection, Fall Detection, Violence Detection, Predictive Analytics, Multi-camera Re-ID, or Automated Incident Reports in Version 1. Design clean abstractions so these can be added seamlessly in future phases.

---

## 4. Quality Assurance & Verification

### Testing & Build Lifecycle
1. **Write Automated Tests:** Maintain unit, integration, and end-to-end test suites covering API endpoints, AI detection, polygon intersection math, loitering state tracking, event/alert creation, and WebSocket emissions.
2. **Run Tests After Changes:** Execute test suites after modifying backend or frontend logic to prevent regressions.
3. **Verify Production Builds:** Ensure both backend (Python tests/lint) and frontend (`vite build`, TypeScript compilation) succeed cleanly before completing any feature phase.
4. **Inspect Logs on Failure:** Always examine full error output and stack traces before diagnosing failures.
5. **Document Decisions:** Record architectural design decisions, schema migrations, and API updates in project documentation under `docs/`.
