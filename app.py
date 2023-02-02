from flask import render_template, Response, request, redirect, flash, session, Flask
from flask_mail import Mail, Message
from empleados import empleados
from usuarios import usuarios
import mediapipe as mp
import cv2
import pymysql

app = Flask(__name__)
app.secret_key = "ab"
app.register_blueprint(empleados)
app.register_blueprint(usuarios)

#Email variables
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'd.i.e.g.o.nambo123@gmail.com'
app.config['MAIL_PASSWORD'] = 'wrxbqljyszwesklc'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)
# msg = Message('Este es tu codigo de confirmacion', sender='d.i.e.g.o.nambo123@gmail.com', recipients=['a18300278@ceti.mx'])
# msg.body = "Hola esta es una prueba de enviar un correo de confirmacion a traves de flask"
# mail.send(msg)

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
                                db='diegomedel$decore')
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

@app.route("/login", methods=["POST"])
def login():
    conexion = connection()
    correo = request.form["correo"]
    contraseña = request.form["contraseña"]
    
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM cuenta WHERE Correo = %s", (correo))
        rows = cursor.fetchall()
        for row in rows:
            session['id_usuario'] = row[0]
            rol = row[1]
            contraseñaC = row[3]
    
    if 'rows' not in vars():
        flash("Correo inexistente")
        return redirect("/")

    if 'contraseñaC' in vars():
        if contraseña != contraseñaC:
            flash("Contraseña incorrecta")
            return redirect("/")
    else:
        return redirect("/")

    if rol == 1:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT Tipo_Empleado FROM empleado WHERE Id_Empleado = %s", (session['id_usuario']))
            rows = cursor.fetchall()
            for row in rows:
                tempId = session['id_usuario']
                session.clear()

                if row[0] == 1:
                    session['id_encargadoCaja'] = tempId
                    return redirect("/caja")
                elif row[0] == 2:
                    session['id_supervisor'] = tempId
                    return redirect("/supervisores")
                elif row[0] == 3:
                    session['id_administrador'] = tempId
                    return redirect("/administradores")
                elif row[0] == 4:
                    session['id_inventario'] = tempId
                    return redirect("/inventario")
    else:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT * FROM usuarios WHERE Id_Usuario = %s", (session['id_usuario']))
            usuario = cursor.fetchone()
        
        conexion.close()

        if usuario is None:
            return redirect("/formulario")
        else:
            if usuario[1] is None:
                return redirect("/formulario")
            return redirect("/usuarios")

@app.route("/formulario")
def formulario():
    if not 'id_usuario' in session: return redirect("/")
    return render_template("usuarios/formulario.html")

@app.route("/guardarDatosUsuario", methods=["POST"])
def guardarDatosUsuario():
    conexion = connection()
    nombre = request.form["nombre"]
    edad = request.form["edad"]
    colorOjos = request.form["colorOjos"]
    tipoPiel = request.form["tipoPiel"]
    colorPiel = request.form["colorPiel"]
    colorCabello = request.form["colorCabello"]

    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO usuarios VALUES(%s, %s, %s, %s, %s, %s, %s, 2)", (session['id_usuario'], nombre, edad, colorOjos, tipoPiel, colorPiel, colorCabello))

    conexion.commit()
    conexion.close()

    return redirect("/usuarios")
    
@app.route("/videoFeed")
def videoFeed():
    return Response(generate(), mimetype="multipart/x-mixed-replace; boundary=frame")

@app.before_request
def before_request():
    ruta = request.path

    if not 'id_usuario' in session and '/usuarios' in ruta:
        return redirect("/")

    if not 'id_administrador' in session and '/administradores' in ruta:
        return redirect("/")

    if not 'id_encargadoCaja' in session and '/caja' in ruta:
        return redirect("/")

    if not 'id_supervisor' in session and '/supervisores' in ruta:
        return redirect("/")

    if not 'id_inventario' in session and '/inventario' in ruta:
        return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="3000")