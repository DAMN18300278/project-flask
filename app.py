from flask import Flask
from flask import render_template
from flask import Response
from flask import request
from flask import redirect
from flask import flash
from flask import url_for
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
import mediapipe as mp
import cv2
import pymysql

app = Flask(__name__)
app.secret_key = "ab"

#Email variables
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'lpipeavila1@gmail.com'
app.config['MAIL_PASSWORD'] = 'sxtxzekzghwwcven'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True 



mail = Mail(app)
#Este valor es como la contraseña del token
s = URLSafeTimedSerializer('decore')

#Mediapipe variables
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

#mysql variables
def connection():
    return pymysql.connect(host='localhost',
                                user='root',
                                password='',
                                db='decore')
#--------------------------------------------------------#

@app.route("/")
def index():
    return render_template("index/login.html")

@app.route("/guardarUsuario", methods=["POST"])
def guardarUsuario():
    conexion = connection()
    correo = request.form["correo"]
    contraseña = request.form["contraseña"]

    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO cuenta VALUES ('', 2, %s, %s)", (correo, contraseña))
    
    conexion.commit()
    conexion.close()

    return redirect("/")

@app.route("/register")
def registrar():
    return render_template("index/register.html")

@app.route("/send_correo", methods=['GET','POST'])
def send_correo():
    if request.method == "POST":
        email = request.form['correo']
        contraseña = request.form['contraseña']
        estado = 'Inactivo'

        conexion = connection()
        with conexion.cursor() as cursor:
            cursor.execute("INSERT INTO cuenta VALUES ('', 2, %s, %s,%s)", (email, contraseña,estado))
        conexion.commit()
        conexion.close()

        token = s.dumps(email, salt='email-confirm')
        subject = 'Confirmacion de Cuenta Decore'
        
        # en el sender hay que poner un correo de decore
        message = Message(subject,sender="lpipeavila1@gmail.com", recipients=[email])
        
        link = url_for('confirm',token=token, _external=True)

        message.body = 'Porfavor ingresa al siguiente link para confirmar la creacion de tu cuenta {}'.format(link)

        mail.send(message)

        success = "Correo enviado"
        return render_template("index/result.html", success=success)

@app.route('/confirm/<token>')
def confirm(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=60)
        conexion = connection()
        with conexion.cursor() as cursor:
            cursor.execute("UPDATE cuenta SET estado = 'Activo' WHERE Correo = (%s)", (email))
        conexion.commit()
        conexion.close()
    except SignatureExpired:
        return '<h1>The token is expired!</h1>'
    return '<h1>The Token Works!</h1>'


@app.route("/login", methods=["POST"])
def login():
    conexion = connection()
    correo = request.form["correo"]
    contraseña = request.form["contraseña"]
    
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM cuenta WHERE Correo = %s", (correo))
        rows = cursor.fetchall()
        for row in rows:
            idCuenta = row[0]
            rol = row[1]
            contraseñaC = row[3]
    
    if 'rows' not in vars():
        flash("Correo inexistente")
        return redirect("/")

    if contraseña != contraseñaC:
        flash("Contraseña incorrecta")
        return redirect("/")

    if rol == 1:
        return redirect("/empleados")
    else:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT * FROM usuarios WHERE Id_Usuario = %s", (idCuenta))
            usuario = cursor.fetchone()
        
        conexion.close()

        if usuario[1] is None:
            return redirect("/formulario")
        else:
            return redirect("/usuarios")
    
@app.route("/usuarios")
def usuarios():
    return render_template("usuarios/usuariosMaster.html")

@app.route("/formulario")
def formulario():
    return render_template("usuarios/formulario.html")

@app.route("/empleados")
def empleados():
    return render_template("empleados/empleadosMaster.html")
    
@app.route("/videoFeed")
def videoFeed():
    return Response(generate(), mimetype="multipart/x-mixed-replace; boundary=frame")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="3000")