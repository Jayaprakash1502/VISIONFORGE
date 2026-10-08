# VISIONFORGE - Review 1 Demonstration Guide

**Project Title:** VISIONFORGE - AI Based Intelligent Video Analytics Platform  
**Team Lead:** Jayaprakash R  
**Team Members:** Jayaprakash R, Harisudhan S, Ezhilarasi K  
**Core Mission:** *"We are not building another CCTV system. We are making existing surveillance systems intelligent."*  

---

## 1. Prerequisites & Environment Check

Before starting the demonstration, ensure:
- Python 3.11.9 installed.
- Node.js v24+ & npm installed.
- `backend/.venv` virtual environment exists with dependencies installed (`fastapi`, `opencv-python`, `ultralytics`, `sqlalchemy`, `pytest`).

---

## 2. Step-by-Step Launch Instructions

### Step 1: Start the Backend FastAPI Server
Open PowerShell Terminal 1:
```powershell
# Navigate to project root:
cd C:\Users\Jayaprakash\OneDrive\Desktop\VISIONIQ

# Set PYTHONPATH and launch FastAPI Uvicorn server:
$env:PYTHONPATH="."
.\backend\.venv\Scripts\python.exe -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```
*Backend API server will be live at: `http://127.0.0.1:8000`*  
*Interactive OpenAPI docs: `http://127.0.0.1:8000/docs`*

### Step 2: Start the Frontend React Development Server
Open PowerShell Terminal 2:
```powershell
# Navigate to frontend folder:
cd C:\Users\Jayaprakash\OneDrive\Desktop\VISIONIQ\frontend

# Launch Vite dev server:
cmd /c "npm run dev"
```
*Frontend SOC Dashboard will be live at: `http://localhost:5173`*

---

## 3. Review 1 Live Demonstration Workflow

1. **Open the Dashboard UI:**
   - Open Chrome / Edge browser to `http://localhost:5173`.
   - Observe the dark Security Operations Center (SOC) theme, VISIONFORGE branding, KPI cards, and stream container.

2. **Start AI Video Analysis:**
   - Click the <strong style="color:#06b6d4">START ANALYSIS</strong> button on the main video panel.
   - OpenCV opens `data/videos/demo.mp4`, and YOLOv8 detects walking person objects frame-by-frame.
   - Green bounding boxes `Person 88%`, person centroids, and live count appear over the video feed!

3. **Verify Polygon Restricted Area Breach Event:**
   - Observe **Restricted Zone A** outlined in orange on the left of the video screen.
   - When a detected person enters Restricted Zone A, the polygon highlights bright RED!
   - `RESTRICTED_AREA_ENTRY` event triggers, and a **HIGH** severity alert appears instantly on the right **ACTIVE ALERTS** panel!

4. **Verify Crowd Detection Event:**
   - As multiple people enter the surveillance scene ($>5$ persons observed), a `CROWD_DETECTED` event triggers.
   - A **HIGH** severity alert appears on the dashboard.

5. **Demonstrate Human-in-the-Loop Operator Actions:**
   - Click **Acknowledge** on an active alert. Notice the status updates from `NEW` to `ACKNOWLEDGED`.
   - Click **Resolve Alert**. Notice the alert moves out of the active list and marks as resolved in event history!

6. **Inspect Event History:**
   - Navigate to the **Events** tab in the top navigation bar.
   - Filter events by type or severity. Click **Details** to open the Event Detail Modal containing detection metadata and timestamp details.

7. **Stop Video Analysis:**
   - Return to the Dashboard and click <strong style="color:#ef4444">STOP ANALYSIS</strong>.
   - OpenCV resources are released safely.
