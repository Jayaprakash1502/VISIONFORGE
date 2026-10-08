import os
import cv2
import numpy as np


def create_demo_surveillance_video(output_path: str = "data/videos/demo.mp4"):
    """
    Generates a synthetic high-quality surveillance video clip with walking person shapes
    that breach polygon zones and simulate crowd density for offline/demo testing.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    width, height = 1280, 720
    fps = 30
    duration_sec = 20
    total_frames = fps * duration_sec
    
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    if not out.isOpened():
        print("Failed to open VideoWriter for path:", output_path)
        return

    print(f"Generating synthetic surveillance video ({width}x{height}, {fps} FPS, {duration_sec}s)...")
    
    # Generate background (Security Lobby / Vault layout)
    background = np.zeros((height, width, 3), dtype=np.uint8)
    # Tiled floor
    for y in range(0, height, 80):
        for x in range(0, width, 80):
            color = (35, 40, 45) if ((x // 80) + (y // 80)) % 2 == 0 else (45, 50, 55)
            cv2.rectangle(background, (x, y), (x + 80, y + 80), color, -1)
    
    # Draw static walls and boundary lines
    cv2.rectangle(background, (0, 0), (width, 80), (20, 25, 30), -1)
    cv2.putText(background, "VISIONFORGE CAM-01 :: VAULT ENTRANCE LOBBY", (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (200, 200, 200), 2)
    
    # Polygon restricted zone outline in background
    pts = np.array([[100, 100], [450, 100], [450, 320], [100, 320]], np.int32)
    cv2.polylines(background, [pts], True, (0, 165, 255), 2)
    cv2.putText(background, "RESTRICTED ZONE A", (110, 130),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 165, 255), 2)

    for i in range(total_frames):
        frame = background.copy()
        t = i / fps
        
        # Person 1: Walking from left to right, entering Restricted Zone A around t=3s to t=12s
        p1_x = int(50 + t * 45)
        p1_y = int(200 + np.sin(t * 2) * 15)
        draw_person(frame, p1_x, p1_y, scale=1.0, color=(220, 220, 220))
        
        # Person 2: Walking top to bottom on the right side
        p2_x = int(600 + np.cos(t * 1.5) * 30)
        p2_y = int(120 + t * 25)
        draw_person(frame, p2_x, p2_y, scale=0.9, color=(200, 220, 200))
        
        # Crowd Wave at t > 10s: Add 4 more people to trigger CROWD_DETECTED (Total 6 people)
        if t > 8.0:
            draw_person(frame, 700, 250, scale=0.95, color=(210, 210, 210))
            draw_person(frame, 780, 280, scale=1.0, color=(190, 210, 230))
            draw_person(frame, 850, 230, scale=0.9, color=(220, 200, 210))
            draw_person(frame, 920, 300, scale=1.05, color=(230, 230, 210))

        out.write(frame)
        
    out.release()
    print(f"Successfully generated demo video: {output_path}")


def draw_person(frame, x, y, scale=1.0, color=(200, 200, 200)):
    """Helper drawing a human silhouette representation."""
    h = int(110 * scale)
    w = int(40 * scale)
    
    # Head
    head_radius = int(12 * scale)
    cv2.circle(frame, (x, y - h + head_radius), head_radius, color, -1)
    
    # Torso
    torso_top = y - h + head_radius * 2
    torso_bottom = y - int(35 * scale)
    cv2.rectangle(frame, (x - w // 2, torso_top), (x + w // 2, torso_bottom), color, -1)
    
    # Legs
    cv2.line(frame, (x - int(10 * scale), torso_bottom), (x - int(15 * scale), y), color, int(6 * scale))
    cv2.line(frame, (x + int(10 * scale), torso_bottom), (x + int(15 * scale), y), color, int(6 * scale))


if __name__ == "__main__":
    create_demo_surveillance_video()
