from flask import Flask, render_template, Response
import cv2
import numpy as np
from ultralytics import YOLO

app = Flask(__name__)

# Load YOLO model
model = YOLO('yolov8s.pt')

# Load class names
with open("coco.txt", "r") as file:
    class_list = file.read().splitlines()

# Define parking areas dynamically
parking_areas = {
    1: [(52, 364), (30, 417), (73, 412), (88, 369)],
    2: [(105, 353), (86, 428), (137, 427), (146, 358)],
    3: [(159, 354), (150, 427), (204, 425), (203, 353)],
    4: [(217, 352), (219, 422), (273, 418), (261, 347)],
    5: [(274, 345), (286, 417), (338, 415), (321, 345)],
    6: [(336, 343), (357, 410), (409, 408), (382, 340)],
    7: [(396, 338), (426, 404), (479, 399), (439, 334)],
    8: [(458, 333), (494, 397), (543, 390), (495, 330)],
    9: [(511, 327), (557, 388), (603, 383), (549, 324)],
    10: [(564, 323), (615, 381), (654, 372), (596, 315)],
    11: [(616, 316), (666, 369), (703, 363), (642, 312)],
    12: [(674, 311), (730, 360), (764, 355), (707, 308)],
    13: [(824, 294), (867, 320), (896, 319), (845, 290)],
}

# Initialize video capture
cap = cv2.VideoCapture('parking1.mp4')

if not cap.isOpened():
    print("Error: Unable to open video file.")
    exit()


def generate_frames():
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, (1020, 500))

        # Run YOLO model predictions
        results = model.predict(frame, conf=0.5)
        if not results:
            print("No predictions made.")
            continue

        # Extract detections
        detections = results[0].boxes.data.cpu().numpy()
        parked_vehicles = {area: 0 for area in parking_areas}  # Initialize counts

        for detection in detections:
            x1, y1, x2, y2, conf, class_id = map(int, detection[:6])
            class_name = class_list[class_id]

            # Process vehicles (cars, trucks, etc.)
            if class_name in ['car', 'truck', 'bus', 'motorbike', 'bicycle']:
                # Calculate center of the bounding box
                cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

                for area_id, coordinates in parking_areas.items():
                    if cv2.pointPolygonTest(np.array(coordinates, np.int32), (cx, cy), False) >= 0:
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.circle(frame, (cx, cy), 3, (0, 0, 255), -1)
                        parked_vehicles[area_id] += 1
                        break

        # Display parking area status
        available_spaces = 0
        for area_id, coordinates in parking_areas.items():
            occupied = parked_vehicles[area_id] > 0
            color = (0, 0, 255) if occupied else (0, 255, 0)
            cv2.polylines(frame, [np.array(coordinates, np.int32)], True, color, 2)
            cv2.putText(frame, str(area_id), coordinates[0], cv2.FONT_HERSHEY_COMPLEX, 0.5, color, 1)
            if not occupied:
                available_spaces += 1

        # Display available spaces
        cv2.putText(frame, f"Available Spaces: {available_spaces}", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (255, 255, 255), 2)

        if cv2.waitKey(500) & 0xFF == 27:  # Exit on 'Esc' key
            break

        # Encode frame to send to client
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True)

