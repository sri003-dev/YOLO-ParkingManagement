# 🚗 Parking‑Lot Monitoring with YOLOv8 + Flask

A lightweight web application that uses **YOLOv8** object detection to track vehicle occupancy in a parking lot, streams the annotated video in real‑time, and displays the number of available spaces on screen.

---

## 🎯 Features

| Feature | Description |
|---------|-------------|
| **Real‑time detection** | Runs YOLOv8 (`yolov8s.pt`) on each video frame to identify cars, trucks, buses, bikes, etc. |
| **Parking‑space status** | Dynamically defined polygons mark each parking spot; the app shows **green** (free) or **red** (occupied) outlines and counts available spots. |
| **Live MJPEG stream** | Frames are encoded as JPEG and served via Flask at `/video_feed`, enabling seamless playback in any browser. |
| **Simple UI** | One‑page HTML (Jinja2 template) with **Start / Stop** controls, custom CSS, and a tiny vanilla‑JS helper script. |

---

## 🧱 Tech Stack

- **Python 3.8+**
- **Flask** – web server & routing  
- **OpenCV (Python)** – frame capture & drawing  
- **ultralytics/YOLOv8** – pre‑trained object‑detection model  
- **NumPy** – geometry checks (`cv2.pointPolygonTest`)  
- **HTML + CSS + JS** – front‑end





