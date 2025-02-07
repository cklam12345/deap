from flask import Flask, render_template, jsonify, request, redirect, url_for, send_file
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import cv2
import requests
import uuid
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
db = SQLAlchemy(app)

class Camera:
    def __init__(self):
        self1 = cv2.VideoCapture(0)  # Use index of camera (0 for default webcam)
        self2 = cv2.VideoCapture(1)  # Use another camera if available
        self cap_list = [self1, self2]
    
    def take_picture(self, face=False):
        images = []
        last_image_path = None
        
        try:
            with requests.Session() as session:
                for cap in self.cap_list:
                    success, image = cap.read()
                    if not success:
                        continue

                    # Face detection
                    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                    faces = face_cascade.detectMultiScale(gray, 1.3, 4)

                    for (x, y, w, h) in faces:
                        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        face ROI
                        face_image = image[y:y+h, x:x+w]
                        cv2.imwrite('face.jpg', face_image)

                    # Capture last image if no faces detected or explicitly requested
                    if not face or len(faces) == 0:
                        cv2.imwrite('last_image.jpg', image)
                        last_image_path = 'last_image.jpg'
        
        except Exception as e:
            logger.error(f"Error capturing image: {e}")
            raise

        return {'images': images, 'last_image_path': last_image_path}

# Initialize camera
camera = Camera()

# Flask App Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///images.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/api/capture', methods=['POST'])
def api_capture():
    data = request.json
    logger.info(f"Received image capture request: {data}")
    
    try:
        # Send images to backend
        response = requests.post(
            'http://localhost:8080/api/upload',
            files={'image': open('face.jpg', 'rb')}
        )
        
        if response.status_code == 200:
            logger.info("Successfully uploaded face image")
            return jsonify({'message': 'Image captured and sent successfully'}), 200
        else:
            logger.error(f"Error uploading image: {response.status_code}")
            return jsonify({'error': f'Failed to upload image - {response.status_code}'}), response.status_code
        
    except Exception as e:
        logger.error(f"Error in api_capture: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/capture/all')
def api_capture_all():
    images = []
    try:
        for cap in camera.cap_list:
            success, image = cap.read()
            if not success:
                continue
            cv2.imwrite(f'camera_{uuid.uuid4()}.jpg', image)
            images.append({'path': f'camera_{uuid.uuid4()}.jpg'})
        
        response = requests.post(
            'http://localhost:8080/api/upload/all',
            files={'images': (None, images)}
        )
        
        if response.status_code == 200:
            logger.info("Successfully uploaded all camera images")
            return jsonify({'message': 'All camera images captured and sent successfully'}), 200
        else:
            logger.error(f"Error uploading camera images: {response.status_code}")
            return jsonify({'error': f'Failed to upload camera images - {response.status_code}'}), response.status_code
        
    except Exception as e:
        logger.error(f"Error in api_capture_all: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/debug')
def api_debug():
    logger.info("Debug request received")
    return jsonify({'message': 'Debug logging enabled'}), 200

if __name__ == '__main__':
    app.run(debug=True)
