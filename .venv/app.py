from flask import Flask 
from flask import Response
from flask import render_template
import cv2
import os 
import time 
import numpy as np



fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc,20.0,(640,480))


# Initialize the webcam
cap = cv2.VideoCapture(0)

# Allow the camera to warm up and capture the initial background
time.sleep(3)
background = 0
count=0
app = Flask(__name__)
# Capture the background
for i in range(60):
    ret, background = cap.read()
    if not ret:
        break

# Flip the background image horizontally
background = np.flip(background, axis=1)

def generate_frames():
    while True:
        # Capture the current frame
        ret, frame = cap.read()
        if not ret:
            break
        count += 1
        
        # Flip the frame horizontally (to mirror the video)
        frame = np.flip(frame, axis=1)
        
        # Convert the frame to HSV color space
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Define the color range for detecting the cloak
        cloak_color_lower = np.array([0, 0, 40])
        cloak_color_upper = np.array([180, 18, 230])

        
        # Create a mask to detect the specific color (cloak color)
        mask = cv2.inRange(hsv, cloak_color_lower, cloak_color_upper)
        
        # Refine the mask using morphological transformations
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8), iterations=2)
        mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, np.ones((3, 3), np.uint8), iterations=1)
        
        # Invert the mask to get the parts of the frame that are not the cloak
        mask_inv = cv2.bitwise_not(mask)
        
        # Extract the cloak area from the background
        cloak_area = cv2.bitwise_and(background, background, mask=mask)
        
        # Extract the current frame's area that does not include the cloak
        non_cloak_area = cv2.bitwise_and(frame, frame, mask=mask_inv)
        
        # Combine the cloak area with the non-cloak area
        final_output = cv2.addWeighted(cloak_area, 1, non_cloak_area, 1, 0)
        
        # Encode the frame as JPEG
        ret, buffer = cv2.imencode('.jpg', final_output)
        frame = buffer.tobytes()
        
        # Yield the frame in a format suitable for streaming
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)