from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from flask import render_template, Response, request, redirect, flash, session, Flask, url_for
from flask_mail import Mail, Message
from empleados import empleados
from usuarios import usuarios
import mediapipe as mp
import paypalrestsdk
import cv2
import babel
import time
from flask_mysqldb import MySQL
from jinja2 import ext

app = Flask(__name__)

app.jinja_env.add_extension(ext.do)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'diegomedel$decore'
app.config["MYSQL_PORT"] = 3306

mysql = MySQL(app)

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
mail = Mail(app)

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

#Este valor es como la contraseña del token
s = URLSafeTimedSerializer('decore')

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

mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh

# Inicializar la detección de rostros y malla facial
face_mesh = mp_face_mesh.FaceMesh()

# Inicializar la captura de video
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

def generate():
    while True:
        # Leer un frame del video
        ret, frame = cap.read()

        # Convertir el frame a RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detectar la malla facial en el frame
        results = face_mesh.process(frame_rgb)

        # Dibujar la malla facial en el frame
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                # Obtener las coordenadas de los puntos de referencia del ojo izquierdo
                left_eye_landmarks = face_landmarks.landmark[35]
                left_eye_x = int(left_eye_landmarks.x * frame.shape[1])
                left_eye_y = int(left_eye_landmarks.y * frame.shape[0])

                # Obtener las coordenadas de los puntos de referencia del ojo derecho
                right_eye_landmarks = face_landmarks.landmark[265]
                right_eye_x = int(right_eye_landmarks.x * frame.shape[1])
                right_eye_y = int(right_eye_landmarks.y * frame.shape[0])

                # Calcular la posición de las pestañas
                eyelash_y = int((left_eye_y + right_eye_y) / 2)

                # Cargar la imagen de las pestañas
                eyelash_img = cv2.imread('intento.png', cv2.IMREAD_UNCHANGED)

                # Escalar la imagen de las pestañas para que se ajuste al tamaño del ojo
                scale_factor = (right_eye_x - left_eye_x) / eyelash_img.shape[1]
                eyelash_img_resized = cv2.resize(eyelash_img, (0, 0), fx=scale_factor, fy=scale_factor)

                # Superponer la imagen de las pestañas en el frame
                x_offset = left_eye_x
                y_offset = eyelash_y - eyelash_img_resized.shape[0]
                alpha_s = eyelash_img_resized[:, :, 3] / 255.0
                alpha_l = 1.0 - alpha_s
                for c in range(0, 3):
                    frame[y_offset:y_offset + eyelash_img_resized.shape[0], x_offset:x_offset + eyelash_img_resized.shape[1], c] = (
                                alpha_s * eyelash_img_resized[:, :, c] + alpha_l * frame[
                            y_offset:y_offset + eyelash_img_resized.shape[0],
                            x_offset:x_offset + eyelash_img_resized.shape[1], c])

        (flag, encodedImage) = cv2.imencode(".jpg", frame)
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

    

@app.route("/send_correo", methods=['GET', 'POST'])
def send_correo():
    if request.method == "POST":
        email = request.form['correo']
        contraseña = request.form['contraseña']
        estado = 'Inactivo'

        # Verificar si ya existe un usuario con el mismo correo electrónico
        with mysql.connection.cursor() as cursor:
            cursor.execute("SELECT Correo FROM cuenta WHERE Correo = %s", (email,))
            existing_user = cursor.fetchone()

        if existing_user:
            # Enviar un correo electrónico de confirmación al usuario existente
            token = s.dumps(email, salt='email-confirm')
            subject = 'Restablecimiento de cuenta Decore'

            message = Message(subject, sender="decore.makeup@gmail.com", recipients=[email])

            link = url_for('confirm', token=token, _external=True)

            message.body = 'Se ha intentado crear una nueva cuenta con este correo electrónico, pero ya existe una cuenta registrada. Si desea restablecer su cuenta, ingrese al siguiente link: {}'.format(link)

            mail.send(message)
            

            return redirect("/")

        else:
            # Insertar el nuevo usuario en la tabla cuenta
            with mysql.connection.cursor() as cursor:
                cursor.execute("INSERT INTO cuenta (Rol, Correo, Contraseña, estado) VALUES (2, %s, %s, %s)", (email, contraseña, estado))
            mysql.connection.commit()

            # Enviar un correo electrónico de confirmación al nuevo usuario
            token = s.dumps(email, salt='email-confirm')
            subject = 'Confirmación de cuenta Decore'

            message = Message(subject, sender="decore.makeup@gmail.com", recipients=[email])

            link = url_for('confirm', token=token, _external=True)

            message.body = 'Por favor, ingrese al siguiente link para confirmar la creación de su cuenta: {}'.format(link)

            mail.send(message)

            return redirect("/")


@app.route('/confirm/<token>')
def confirm(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=600)
        with mysql.connection.cursor() as cursor:
            cursor.execute("UPDATE cuenta SET estado = 'Activo' WHERE Correo = (%s)", (email,))
        mysql.connection.commit()
        return redirect("/")
    except SignatureExpired:
        return '<h1>The token is expired!</h1>'

    return '<h1>The Token Works!</h1>'

@app.route('/confirmrecover/<token>')
def confirmrecover(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age = 600)
              
    except SignatureExpired:
        return '<h1>The link is expired!</h1>'
    return render_template("index/cambiarcontrasena.jinja", correo =email)

@app.route("/login", methods=["POST"])
def login():
    cursor = mysql.connect.cursor()
    correo = request.form["correo"]
    contraseña = request.form["contraseña"]
    
    cursor.execute("SELECT * FROM cuenta WHERE Correo = %s", (correo,))
    rows = cursor.fetchone()
        
    if rows is None:
        flash("Correo inexistente")
        return redirect("/")
    
    session['id_usuario'] = rows[0]
    rol = rows[1]
    contraseñaC = rows[3]

    if 'contraseñaC' in vars():
        if contraseña != contraseñaC:
            flash("Contraseña incorrecta")
            return redirect("/")
    else:
        return redirect("/")

    if rol == 1:
        cursor.execute("SELECT Tipo_Empleado FROM empleado WHERE Id_Empleado = %s", (session.get('id_usuario'),))
        rows = cursor.fetchone()
        tempId = session.get('id_usuario')
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
            cursor.execute("SELECT * FROM usuarios WHERE Id_Usuario = %s", (session.get('id_usuario'),))
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
        cursor.execute("INSERT INTO usuarios VALUES(%s, %s, %s, %s, %s, %s, %s, 2)", (session.get('id_usuario'), nombre, edad, colorOjos, tipoPiel, colorPiel, colorCabello))

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

    if not 'id_usuario' in session and '/usuarios' in ruta:
        return redirect("/")

    if not 'id_administrador' in session and '/administradores' in ruta:
        return redirect("/")

    if not 'id_encargadoCaja' in session and '/caja' in ruta:
        return redirect("/")

    if not 'id_supervisor' in session and '/supervisores' in ruta:
        return redirect("/")

    if not 'id_inventario' in session and '/eInventario' in ruta:
        return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="3000")