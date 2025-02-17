from flask import Flask, request, send_file
import cv2
import numpy as np
import io

app = Flask(__name__)

# Load OpenCV’s pre-trained face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

def blur_faces(image_bytes):
    image_array = np.asarray(bytearray(image_bytes), dtype=np.uint8)
    img = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    faces = face_cascade.detectMultiScale(img, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    for (x, y, w, h) in faces:
        face_region = img[y:y+h, x:x+w]
        blurred_face = cv2.GaussianBlur(face_region, (99, 99), 30)
        img[y:y+h, x:x+w] = blurred_face

    _, img_encoded = cv2.imencode('.jpg', img)
    return io.BytesIO(img_encoded)

@app.route("/blur", methods=["POST"])
def blur_image():
    if "image" not in request.files:
        return {"error": "No image uploaded"}, 400

    image_file = request.files["image"].read()
    blurred_image = blur_faces(image_file)
    return send_file(blurred_image, mimetype='image/jpeg')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
