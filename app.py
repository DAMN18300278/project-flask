from sys import flags
from flask import Flask
from flask import render_template
from flask import Response
import mediapipe as mp
import cv2

app = Flask(__name__)
mpFaceMesh = mp.solutions.face_mesh
mpDrawing = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)

def generate():
    with mpFaceMesh.FaceMesh(
        static_image_mode = False,
        max_num_faces = 1,
        min_detection_confidence = 0.2) as faceMesh:
        while True:
            ret, image = cap.read()
            if ret == False:
                break

            image = cv2.flip(image, 1)
            imageRgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = faceMesh.process(imageRgb)
            
            if results.multi_face_landmarks is not None:
                for fL in results.multi_face_landmarks:
                    mpDrawing.draw_landmarks(
                        image, 
                        fL, 
                        mpFaceMesh.FACEMESH_CONTOURS, 
                        mpDrawing.DrawingSpec(color=(255, 0, 100), thickness=1, circle_radius=1),
                        mpDrawing.DrawingSpec(color=(255, 100, 0), thickness=1))
            (flag, encodedImage) = cv2.imencode(".jpg", image)
            if not flag:
                continue
            yield(b'--frame\r\n' b'Content-Type: image\jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/videoFeed")
def videoFeed():
    return Response(generate(), 
        mimetype="multipart/x-mixed-replace; boundary=frame")

if __name__ == "__main__":
    app.run(debug=True)