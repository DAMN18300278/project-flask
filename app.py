
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from flask import render_template, Response, request, redirect, flash, session, Flask, url_for
from flask_mail import Mail, Message
from empleados import empleados
from usuarios import usuarios
import mediapipe as mp
import paypalrestsdk
import cv2
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = "ab"
app.register_blueprint(empleados)
app.register_blueprint(usuarios)

#Email variables
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'decore.makeup@gmail.com'
app.config['MAIL_PASSWORD'] = 'dtcnejovtwzeozhr'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True 

# Configura las credenciales de PayPal en tu archivo de configuración de Flask
app.config['PAYPAL_MODE'] = 'sandbox' # 'sandbox' o 'live'
app.config['PAYPAL_CLIENT_ID'] = 'TU_CLIENT_ID_DE_PAYPAL'
app.config['PAYPAL_CLIENT_SECRET'] = 'TU_CLIENT_SECRET_DE_PAYPAL'
app.config['PAYPAL_CURRENCY'] = 'MXN' # La moneda que utilizarás para los pagos

# Inicializa la biblioteca de PayPal con las credenciales de tu archivo de configuración
paypalrestsdk.configure({
    "mode": app.config['PAYPAL_MODE'],
    "client_id": app.config['PAYPAL_CLIENT_ID'],
    "client_secret": app.config['PAYPAL_CLIENT_SECRET']
})


#mysql-variables----------------------------------#
mysql = MySQL(app)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'diegomedel$decore'

#--------------------------------------------------#

mail = Mail(app)
#Este valor es como la contraseña del token
s = URLSafeTimedSerializer('decore')

#Mediapipe variables
mpFaceMesh = mp.solutions.face_mesh
mpDrawing = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)

@app.route('/procesar_pago', methods=['POST'])
def procesar_pago():
    # Obtiene el monto del pago desde el formulario de la solicitud POST
    total = request.form['total']

    # Crea un pago en PayPal utilizando la biblioteca de PayPal
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "transactions": [
            {
                "amount": {
                    "total": total,
                    "currency": app.config['PAYPAL_CURRENCY']
                },
                "description": "Pago por orden"
            }
        ],
        "redirect_urls": {
            "return_url": "http://localhost:5000/pago_exitoso",
            "cancel_url": "http://localhost:5000/pago_cancelado"
        }
    })

    # Intenta crear el pago y redirige al usuario a la página de pago de PayPal
    if payment.create():
        for link in payment.links:
            if link.method == "REDIRECT":
                return redirect(link.href)
    else:
        flash("Error al procesar el pago: {}".format(payment.error))
        return redirect(url_for('carrito_compras'))

@app.route('/pago_exitoso')
def pago_exitoso():
    # Renderiza una página de éxito después de que el usuario haya completado el pago
    return render_template('pago_exitoso.html')

@app.route('/pago_cancelado')
def pago_cancelado():
    # Renderiza una página de cancelación si el usuario ha cancelado el pago
    return render_template('pago_cancelado.html')

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
    return render_template("index/login.jinja")

@app.route('/cambiarcontra', methods=["POST"])
def cambiarcontra():
    if request.method == "POST":
        correo = request.form["correo"]
        contraseña = request.form["contraseña"]

        with mysql.connection.cursor() as cursor:
            cursor.execute("UPDATE cuenta SET Contraseña = (%s) WHERE Correo = (%s)", (contraseña,correo))

        mysql.connection.commit()

        return redirect("/")

@app.route("/recover")
def recover():
    return render_template("index/recover.jinja")

@app.route("/register")
def registrar():
    return render_template("index/register.jinja")

@app.route("/send_correo", methods=['GET','POST'])
def send_correo():
    if request.method == "POST":
        email = request.form['correo']
        contraseña = request.form['contraseña']
        estado = 'Inactivo'

        with mysql.connection.cursor() as cursor:
            cursor.execute("INSERT INTO cuenta VALUES ('', 2, %s, %s,%s)", (email, contraseña,estado))
        mysql.connection.commit()

        token = s.dumps(email, salt='email-confirm')
        subject = 'Confirmacion de Cuenta Decore'
        
        # en el sender hay que poner un correo de decore
        message = Message(subject,sender="decore.makeup@gmail.com", recipients=[email])
        
        link = url_for('confirm',token=token, _external=True)

        message.body = 'Porfavor ingresa al siguiente link para confirmar la creacion de tu cuenta {}'.format(link)

        mail.send(message)

        success = "Correo enviado"
        return redirect("/")

#correocon es para recuperar la contraseña
@app.route("/send_correocon", methods=['POST'])
def send_correocon():
    if request.method == "POST":
        email = request.form['correorecover']

        token = s.dumps(email, salt='email-confirm')
        subject = 'Cambio de contraseña Decore'
        
        # en el sender hay que poner un correo de decore
        message = Message(subject,sender="decore.makeup@gmail.com", recipients=[email])
        
        link = url_for('confirmrecover',token=token, _external=True)

        message.body = 'Porfavor ingresa al siguiente link para confirmar el cambio de contraseña en su cuenta {}'.format(link)

        mail.send(message)

        success = "Correo enviado"
        return redirect("/")

@app.route('/confirm/<token>')
def confirm(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=120)
        with mysql.connection.cursor() as cursor:
            cursor.execute("UPDATE cuenta SET estado = 'Activo' WHERE Correo = (%s)", (email,))
        mysql.connection.commit()
    except SignatureExpired:
        return '<h1>The token is expired!</h1>'
    return '<h1>The Token Works!</h1>'

@app.route('/confirmrecover/<token>')
def confirmrecover(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age = 120)
              
    except SignatureExpired:
        return '<h1>The link is expired!</h1>'
    return render_template("index/cambiarcontrasena.jinja", correo =email)

@app.route("/login", methods=["POST"])
def login():
    cursor = mysql.connection.cursor()
    correo = request.form["correo"]
    contraseña = request.form["contraseña"]
    
    cursor.execute("SELECT * FROM cuenta WHERE Correo = %s", (correo,))
    rows = cursor.fetchone()
        
    session['id_usuario'] = rows[0]
    rol = rows[1]
    contraseñaC = rows[3]
    
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
        cursor.execute("SELECT Tipo_Empleado FROM empleado WHERE Id_Empleado = %s", (session['id_usuario'],))
        rows = cursor.fetchone()
        tempId = session['id_usuario']
        session.clear()

        if rows[0] == 1:
            session['id_encargadoCaja'] = tempId
            return redirect("/caja")
        elif rows[0] == 2:
            session['id_supervisor'] = tempId
            return redirect("/supervisores")
        elif rows[0] == 3:
            session['id_administrador'] = tempId
            return redirect("/administradores")
        elif rows[0] == 4:
            session['id_inventario'] = tempId
            return redirect("/inventario")
    else:
        with mysql.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM usuarios WHERE Id_Usuario = %s", (session['id_usuario'],))
            usuario = cursor.fetchone()

        if usuario is None:
            return redirect("/formulario")
        else:
            if usuario[1] is None:
                return redirect("/formulario")
            return redirect("/usuarios")

@app.route("/formulario")
def formulario():
    if not 'id_usuario' in session: return redirect("/")
    return render_template("usuarios/formulario.jinja")

@app.route("/guardarDatosUsuario", methods=["POST"])
def guardarDatosUsuario():
    nombre = request.form["nombre"]
    edad = request.form["edad"]
    colorOjos = request.form["colorOjos"]
    tipoPiel = request.form["tipoPiel"]
    colorPiel = request.form["colorPiel"]
    colorCabello = request.form["colorCabello"]

    with mysql.connection.cursor() as cursor:
        cursor.execute("INSERT INTO usuarios VALUES(%s, %s, %s, %s, %s, %s, %s, 2)", (session['id_usuario'], nombre, edad, colorOjos, tipoPiel, colorPiel, colorCabello))

    mysql.connection.commit()

    return redirect("/usuarios")
    
@app.route("/videoFeed")
def videoFeed():
    return Response(generate(), mimetype="multipart/x-mixed-replace; boundary=frame")

@app.route("/camara")
def camara():
    return render_template("usuarios/cam.jinja")

#@app.before_request
def before_request():
    ruta = request.path

    print(f"{ruta}  {session}")
    if not 'id_usuario' in session and '/usuarios' in ruta:
        return redirect("/")

    if not 'id_administrador' in session and '/administradores' in ruta:
        print("True")
        return redirect("/")

    if not 'id_encargadoCaja' in session and '/caja' in ruta:
        return redirect("/")

    if not 'id_supervisor' in session and '/supervisores' in ruta:
        return redirect("/")

    if not 'id_inventario' in session and '/eInventario' in ruta:
        return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="3000")