from flask import Flask, jsonify
import cv2

app = Flask(__name__)

# Initialize the video capture
cap = cv2.VideoCapture(0)  # 0 is the index of the camera

@app.route('/take_picture', methods=['GET'])
def take_picture():
    ret, frame = cap.read()
    if ret:
        file_path = '/path/to/store/picture.jpg'  # Change this to your desired file path
        cv2.imwrite(file_path, frame)
        return jsonify({'status': 'success', 'file_path': file_path})
    else:
        return jsonify({'status': 'error', 'message': 'Failed to take picture'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
