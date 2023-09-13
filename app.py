from flask import Flask, render_template, request, redirect, url_for, Response
import cv2
import mediapipe as mp
import os
import base64
import numpy as np  # Import NumPy

app = Flask(__name__)

# Initialize MediaPipe 
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Function to estimate pose from an uploaded image
def estimate_pose_from_image(image):
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        # Convert the image to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Process the image with MediaPipe BlazePose
        results = pose.process(image_rgb)

        # Draw landmarks on the image
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(
                image,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2),
            )

        # Encode the image as JPEG
        ret, buffer = cv2.imencode('.jpg', image)
        frame = buffer.tobytes()

        # Return the processed frame
        return frame

@app.route('/')
def index():
    return render_template('index.html', result=None)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'photo' in request.files:
        photo = request.files['photo']
        if photo.filename != '':
            # Read the uploaded image
            image = cv2.imdecode(np.fromstring(photo.read(), np.uint8), cv2.IMREAD_COLOR)
            
            # Estimate pose and display the result
            result_frame = estimate_pose_from_image(image)
            result = base64.b64encode(result_frame).decode("utf-8")
            
            return render_template('index.html', result=result)
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
