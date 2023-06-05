from flask import Flask, render_template, Response
import cv2
import mediapipe as mp

app = Flask(__name__)

# Initialize MediaPipe 
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Initialize the video capture
cap = cv2.VideoCapture(0)  # Change to the appropriate camera index if necessary

def generate_frames():
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while True:
            # Read frame from the camera
            success, image = cap.read()
            if not success:
                break

            # Convert the image to RGB
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Process the image with MediaPipe BlazePose
            results = pose.process(image_rgb)

            # Draw landmarks on the image
            image_output = image.copy()
            if results.pose_landmarks:
                mp_drawing.draw_landmarks(
                    image_output,
                    results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                    mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2),
                )

            # Encode the image as JPEG
            ret, buffer = cv2.imencode('.jpg', image_output)
            frame = buffer.tobytes()

            # Yield the frame as a response
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
