from flask import Flask, render_template, request, Response
import cv2
import numpy as np

app = Flask(__name__)

# Load your OpenCV model or initialize variables here

@app.route('/')
def index():
    return render_template(r'C:\Users\Hp\Desktop\invisibility\.venv\index.html')

#@app.route('/process', methods=['POST'])
#def process():
    #frame = cv2.imdecode(np.frombuffer(request.files['image'].read(), np.uint8), cv2.IMREAD_COLOR)
    # Apply your OpenCV operations here
    #background = cv2.bitwise_and(frame, frame, mask=mask)
    # Convert the output to JPEG format
    #ret, jpeg = cv2.imencode('.jpg', background)
    #return Response(jpeg.tobytes(), mimetype='image/jpeg')

if __name__ == '__main__':

    app.run(debug=True)

