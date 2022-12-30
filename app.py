from flask import Flask
from flask import render_template
from flask import Response
from PIL import Image
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
        min_detection_confidence = 0.1) as faceMesh:
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

            if image.shape[0] > image.shape[1]:
                image = cv2.add(image, cv2.resize(marco, (image.shape[1], image.shape[0])))
            else:
                image = cv2.resize(image, (1300, 1000))
                image = image[0:1000, 350:950]

                marco = cv2.imread('contorno.png')
                marco = cv2.resize(marco, (600, 600))

                imageCut = image[200:800, 0:600]
                imagenMezcla = cv2.addWeighted(imageCut, 1, marco, 1, 0)

                image[200:800, 0:600] = imagenMezcla

            #if(results.multi_face_landmarks[264])

            (flag, encodedImage) = cv2.imencode(".jpg", image)
            if not flag:
                continue
            yield(b'--frame\r\n' b'Content-Type: image\jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n')

@app.route("/")
def index():
    return render_template("login.html")

@app.route("/videoFeed")
def videoFeed():
    return Response(generate(), 
        mimetype="multipart/x-mixed-replace; boundary=frame")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="3000")