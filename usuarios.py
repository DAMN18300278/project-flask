import flask
import requests
from flask import session, render_template, redirect, jsonify, make_response, url_for, request, flash, Response
from flask_mysqldb import MySQL
from collections import OrderedDict
import base64
from flask_mail import Mail, Message
from datetime import datetime
import cv2
import numpy as np
import base64
import mediapipe as mp
import math

usuarios = flask.Blueprint('usuarios', __name__)
mysql = MySQL()
mail = Mail()

# Inicializar el modelo FaceMesh de MediaPipe
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh()

# Inicializar el modelo FaceMesh de MediaPipe
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh()

def asignarNombre():
    with mysql.connect.cursor() as cursor:
        cursor.execute('SELECT Nombre FROM usuarios WHERE Id_usuario = %s', (session.get('id_usuario'),))
        rows = cursor.fetchone()
        nombre = rows[0]
        return nombre

@usuarios.record_once
def on_load(state):
    app = state.app
    mysql.init_app(app)
    mail.init_app(app)

@usuarios.route("/productsApi")
@usuarios.route("/productsApi/<id>", methods=['GET'])
def productsApi(id=0):
    keys = [
    'Id',
    'Nombre', 
    'Imagenes',
    'Descripcion',
    'Precio u.',
    'Nombre color',
    'Hex color',
    'Categoria',
    'Recomendacion',
    'Marca',
    'Stock',
    'Tipo de piel',
    'Imagenes filtro',
    'Tipo'
    ]
    
    arr = []
    colors = {}


    with mysql.connect.cursor() as cursor:
        if id != 0:
            cursor.execute("SELECT * FROM productos WHERE Id_Productos = %s", (id,))
            rows = cursor.fetchone()
            ord = OrderedDict(zip(keys, rows))
            # Dividir los nombres de colores y los valores de Hex
            color_names = ord['Nombre color'].split(',')
            hex_values = ord['Hex color'].split(',')

            # Crear un nuevo JSON para cada color
            colors = {}
            for i, name in enumerate(color_names):
                colors[i+1] = {'Nombre': name, 'Hex': hex_values[i]}

            # Reemplazar 'Nombre color' y 'Hex color' con el nuevo JSON
            ord['Colores'] = colors
            del ord['Nombre color']
            del ord['Hex color']
            arr.append(ord)

        else:
            cursor.execute("SELECT * FROM productos")
            rows = cursor.fetchall()
            for item in rows:
                ord = OrderedDict(zip(keys, item))
                # Dividir los nombres de colores y los valores de Hex
                color_names = ord['Nombre color'].split(',')
                hex_values = ord['Hex color'].split(',')

                # Crear un nuevo JSON para cada color
                colors = {}
                for i, name in enumerate(color_names):
                    colors[i+1] = {'Nombre': name, 'Hex': hex_values[i]}

                # Reemplazar 'Nombre color' y 'Hex color' con el nuevo JSON
                ord['Colores'] = colors
                del ord['Nombre color']
                del ord['Hex color']

                arr.append(ord)

    response = make_response(jsonify({
            'Productos': arr
        }), 200)

    response.headers["Content-type"] = "application/json"
    return response

@usuarios.route("/usuarios")
def index():
    nombre = asignarNombre()
    link = url_for('usuarios.productsApi', _external=True)
    response = requests.get(link).json()
    data = response['Productos']


    link2 = url_for('usuarios.productsApiordenar', _external=True, id ="1", idUsuario = session.get("id_usuario"))
    response2 = requests.get(link2).json()
    data2 = response2['Productos']

    link3 = url_for('usuarios.productsApiordenar', _external=True, id ="2", idUsuario = session.get("id_usuario"))
    response3 = requests.get(link3).json()
    data3 = response3['Productos']

    link4 = url_for('usuarios.productsApiordenar', _external=True, id ="3", idUsuario = session.get("id_usuario"))
    response4 = requests.get(link4).json()
    data4 = response4['Productos']
    print(link4)

    with mysql.connect.cursor() as cursor:
        cursor.execute("SELECT Carrito FROM usuarios WHERE Id_Usuario = %s", (session.get('id_usuario'),))
        fetch = cursor.fetchone()
        if fetch is None or not fetch[0]:
            numero = 0
        else:
            carritoNum = fetch[0].split("|")
            numero = len(carritoNum)

    
    return render_template("usuarios/landing.jinja", recomendados=data4, populares=data3, ventas = data2, productos = data, idUsuario = session.get('id_usuario'), carrito = numero,nombre = nombre)


@usuarios.route("/usuarios/addcarrito", methods=['POST', 'GET'])
def addcarrito():
    carritoData = request.form['carritoData']
    print(carritoData)
    idUsuario = session.get('id_usuario')
    with mysql.connect.cursor() as cursor:
        cursor.execute("SELECT Carrito FROM usuarios WHERE Id_Usuario = %s", (session.get('id_usuario'),))
        fetch = cursor.fetchone()
        if fetch is None or not fetch[0]:
            carritoData = carritoData.replace("|", "",1)
    with mysql.connection.cursor() as cursor:
        cursor.execute("UPDATE usuarios SET Carrito = CONCAT(Carrito, %s) WHERE id_Usuario = %s", (carritoData, idUsuario))
        mysql.connection.commit()
        
    return redirect("/")

@usuarios.route('/usuarios/kits')
def kits():
    nombre = asignarNombre()
    link = url_for('usuarios.productsApi', _external=True)
    response = requests.get(link).json()
    data = response['Productos']

    for producto in data:
        del producto['Descripcion']
        del producto['Imagenes']
        del producto['Marca']
        del producto['Tipo de piel']
        del producto['Imagenes filtro']
        del producto['Tipo']
        del producto['Recomendacion']


    with mysql.connect.cursor() as cursor:
        cursor.execute("SELECT Carrito FROM usuarios WHERE Id_Usuario = %s", (session.get('id_usuario'),))
        fetch = cursor.fetchone()
        if fetch is None or not fetch[0]:
            numero = 0
        else:
            abubu = fetch[0].split("|")
            numero = len(abubu)
    return render_template("usuarios/kits.jinja", productos = data, idUsuario = session.get('id_usuario'), carrito = numero,nombre = nombre)

@usuarios.route('/usuarios/eliminar_producto/<string:id>', methods=['POST'])
def eliminar_producto(id):
    ids = id.split('_')
    id_producto = int(ids[0])-1
    id = ids[1]
    with mysql.connect.cursor() as cursor:
        cursor.execute("SELECT Carrito FROM usuarios WHERE Id_Usuario = %s",(id,))
        fetch = cursor.fetchone()
        print(fetch)
        carrito = fetch[0].split('|')

        if not carrito:
            flash("Tu carrito esta vacio")
            return redirect("/usuarios/ordencarrito/"+ id)
        del carrito[id_producto]
        carrito_str = '|'.join(carrito)
    with mysql.connection.cursor() as cursor:
        cursor.execute("UPDATE usuarios SET Carrito = %s WHERE id_Usuario = %s", (carrito_str, id))
        mysql.connection.commit()
        
        
    return 'OK'

@usuarios.route("/usuarios/ordencarrito/<string:id>", methods=['POST','GET'])
def ordencarrito(id):

    with mysql.connect.cursor() as cursor:
        
        cursor.execute("SELECT Carrito FROM usuarios WHERE Id_Usuario = %s", (id,))
        fetch = cursor.fetchone()
        if not fetch or not fetch[0]:
            numero = 0
            productos = []
        else:
            
            carrito = fetch[0].split('|') 
            
            
            numero = len(carrito)
            productos = []
            i = 0
            for producto in carrito:
                
                producto = producto.split(',')
                productos.append(producto)
                cursor.execute("SELECT Color_RGBA FROM productos WHERE Id_Productos = %s",(producto[0],))
                fetch = cursor.fetchone()
                if fetch:
                    color = fetch[0].split(',')
                else:
                    color = []
                
                producto[2] = int(producto[2])
                indice_color = int(producto[2])-1

                productos[i].append(color[indice_color])

                #print(color[int(productos[int(productos[i][2])])])
                cursor.execute("SELECT Nombre,Precio FROM productos WHERE Id_Productos = %s", (productos[i][0],))
                datos = cursor.fetchone()
                
                productos[i].extend(datos)

                i+=1
        cursor.execute("SELECT Nombre FROM usuarios WHERE Id_Usuario = %s",(id,))    
        nombre = cursor.fetchone()[0]
        
    return render_template("usuarios/CarritoCompras.jinja",id=id,numero = numero,productos=productos, nombre=nombre)

@usuarios.route("/usuarios/OrdenEspecifica/RecogerCaja/<string:id>", methods=['GET'])
def RecogerCaja(id):
    productos = []
    with mysql.connect.cursor() as cursor:
        cursor.execute("SELECT Estatus_Pedido FROM usuarios WHERE Id_Usuario = %s", (id,))
        result = cursor.fetchone()
      
        if result and result[0] == 'activo':  # Verificar si existe el registro y si el estatus es 'activo'
            
            flash('pedido activo.')
            return redirect("/usuarios/ordencarrito/"+id)
        else:
            with mysql.connect.cursor() as cursor:
                cursor.execute("SELECT carrito From usuarios where Id_Usuario = %s",(id,))
                fetch = cursor.fetchone()
                carrito = fetch[0].split('|') 
                
                numero = len(carrito)
                
                i = 0
                for producto in carrito:
                    producto = producto.split(',')
                    productos.append(producto)
                 
                    with mysql.connect.cursor() as cursor:
                        cursor.execute("SELECT Cantidad From productos where Id_Productos = %s",(producto[0],))
                        cantidad = int(cursor.fetchone()[0])
                       
                        if cantidad > int(producto[1]) :
                            cantidad = cantidad - int(producto[1])

                            with mysql.connection.cursor() as cursor:
                                cursor.execute("UPDATE productos SET Cantidad = %s WHERE Id_Productos = %s", (cantidad,producto[0]))
                        else:
                                flash('No hay suficiente cantidad del producto solicitado')
                                return redirect("/usuarios/ordencarrito/"+id)
            with mysql.connection.cursor() as cursor:
                cursor.execute("UPDATE usuarios SET carrito = '' WHERE Id_Usuario = %s", (id,))
                cursor.execute("UPDATE usuarios SET Estatus_Pedido = 'activo' WHERE Id_Usuario = %s", (id,))
                mysql.connection.commit()
            with mysql.connection.cursor() as cursor:
                cursor.execute("INSERT INTO ordenpago( Id_Usuario, Fecha, Status, carrito) VALUES ( %s, NOW(), 'Pagar en caja', %s)", (id,fetch))
                mysql.connection.commit()
        numeroorden(id)
        actualizaredad(id)
    return redirect("/usuarios")

@usuarios.route("/usuarios/foro")
def foro():
    nombre = asignarNombre()
    link = url_for('usuarios.productsApi', _external=True)
    response = requests.get(link).json()
    data = response['Productos']

    with mysql.connect.cursor() as cursor:
        cursor.execute("SELECT foro.*, usuarios.Nombre FROM foro INNER JOIN usuarios ON foro.Id_usuario = usuarios.Id_Usuario")
        forum = cursor.fetchall()

    return render_template("usuarios/foro.jinja", productos = data, nombre = nombre, forum = forum)

@usuarios.route("/usuarios/guardarPub", methods=['POST', 'GET'])
def guardarPub():
    Id_usuario = session.get('id_usuario')
    Id_producto = request.form['Id_producto']
    Descripcion = request.form['Descripcion']
    Puntuacion = request.form['Puntuacion']

    print(Id_usuario, Id_producto, Descripcion, Puntuacion)

    with mysql.connection.cursor() as cursor:
        cursor.execute("INSERT INTO foro(Id_usuario, Id_producto, Descripcion, Calificacion, Fecha) VALUES(%s,%s,%s,%s, CURDATE())", (Id_usuario, Id_producto, Descripcion, Puntuacion))
        mysql.connection.commit()
    actualizar_promedios()
    return redirect("/")

def takeProfileInfo(id = 0):
    with mysql.connect.cursor() as cursor:
        if id == 0:
            cursor.execute("SELECT * FROM usuarios WHERE Id_Usuario = %s", (session.get("id_usuario"),))
        else:
            cursor.execute("SELECT * FROM usuarios WHERE Id_Usuario = %s", (id,))
        profileInfo = cursor.fetchone()

    return profileInfo

@usuarios.route("/usuarios/perfil")
def perfil():
    profileInfo = takeProfileInfo()
    
    if profileInfo[7] == 'activo':
        with mysql.connect.cursor() as cursor:
            cursor.execute("SELECT Id_Orden FROM ordenpago WHERE Id_Usuario = %s ORDER BY Id_Orden DESC", (session.get('id_usuario'),))
            id_orden = cursor.fetchone()
        return render_template("usuarios/perfil.jinja", profileInfo = profileInfo, id_orden = id_orden)
    return render_template("usuarios/perfil.jinja", profileInfo = profileInfo)

@usuarios.route("/usuarios/updateProfile")
def updateProfile():
    profileInfo = takeProfileInfo()
    with mysql.connect.cursor() as cursor:
        cursor.execute("SELECT Color_Ojos, Hex FROM color_ojos WHERE Id_ColorOjos = %s", (profileInfo[3],))
        coloresOjos = cursor.fetchone()
        cursor.execute("SELECT Tipo_Piel FROM tipo_piel WHERE Id_TipoPiel = %s", (profileInfo[4],))
        tiposPiel = cursor.fetchone()
        
    return render_template("usuarios/formulario.jinja", profileInfo = profileInfo, coloresOjos = coloresOjos, tiposPiel = tiposPiel)

@usuarios.route("/usuarios/updateDatosUsuario", methods=['POST'])
def updateDatosUsuario():
    nombre = request.form["nombre"]
    edad = request.form["edad"]
    colorOjos = request.form["colorOjos"]
    tipoPiel = request.form["tipoPiel"]
    colorPiel = request.form["colorPiel"]
    colorPielForm = request.form["colorPielForm"]
    colorCabello = request.form["colorCabello"]
    with mysql.connection.cursor() as cursor:
        cursor.execute("UPDATE usuarios SET Nombre = %s, Edad = %s, Color_Ojos = %s, Tipo_Piel = %s, Tono_Piel = %s, Color_Pelo = %s, Tono_Piel_Form = %s WHERE Id_Usuario = %s",
                       (nombre, edad, colorOjos, tipoPiel, colorPiel, colorCabello, colorPielForm, session.get('id_usuario')))
        mysql.connection.commit()

    return redirect("/usuarios/perfil")

# Función para calcular el ángulo entre dos puntos
def calcular_angulo(landmarks, frame):
    # Obtener las coordenadas de los puntos clave relevantes
    # Aquí puedes ajustar los índices de los puntos clave según tus necesidades
    p1 = (int(landmarks[10].x * frame.shape[1]), int(landmarks[10].y * frame.shape[0]))
    p2 = (int(landmarks[200].x * frame.shape[1]), int(landmarks[200].y * frame.shape[0]))
    angulo_rad = math.atan2(p2[1] - p1[1], p2[0] - p1[0])
    angulo_deg = math.degrees(angulo_rad)

    # Verificar si el ángulo cumple con tu criterio de orientación
    if angulo_deg <= 93 and angulo_deg >= 87:
        oriented = 1
    else:
        oriented = 0
    return oriented

def detectFaceShape(face_landmarks):
    # Define las proporciones para cada forma de rostro
    proportions = {
        'Ovalado': [0.82, 1.18],
        'Redondo': [1.0, 1.0],
        'Cuadrado': [1.0, 1.0],
        'Rectangular': [1.35, 1.0],
        'Triángulo invertido': [0.9, 1.0],
        'Triangular': [1.1, 1.0],
        'Diamante': [0.95, 1.05]
    }

    # Calcula las proporciones del rostro
    width = face_landmarks.landmark[454].x - face_landmarks.landmark[234].x
    height = (face_landmarks.landmark[10].y - face_landmarks.landmark[152].y) * -1

    # Compara las proporciones del rostro con las proporciones definidas para cada forma
    shape_distances = {}
    for shape, shape_proportions in proportions.items():
        shape_width = shape_proportions[0]
        shape_height = shape_proportions[1]
        distance = abs((width / height) - (shape_width / shape_height))
        shape_distances[shape] = distance
    
    # Encuentra la forma con la distancia más cercana
    face_shape = min(shape_distances, key=shape_distances.get)
    return face_shape

def waysToMakeup(face_landmarks, image):
    face_shape = detectFaceShape(face_landmarks)

    lightSection1 = (109, 108, 9, 337, 338, 10, 109)
    lightSection2 = (8, 196, 4, 419, 8)
    lightSection3 = (31, 118, 119, 120, 121, 233, 232, 231, 230, 229, 228, 31)
    lightSection4 = (261, 347, 348, 349, 350, 453, 452, 451, 450, 449, 448, 261)
    lightSection5 = (18, 83, 201, 199, 421, 313, 18)
    
    suject1 = np.array([(face_landmarks.landmark[i].x * image.shape[1], face_landmarks.landmark[i].y * image.shape[0]) for i in lightSection1])
    suject2 = np.array([(face_landmarks.landmark[i].x * image.shape[1], face_landmarks.landmark[i].y * image.shape[0]) for i in lightSection2])
    suject3 = np.array([(face_landmarks.landmark[i].x * image.shape[1], face_landmarks.landmark[i].y * image.shape[0]) for i in lightSection3])
    suject4 = np.array([(face_landmarks.landmark[i].x * image.shape[1], face_landmarks.landmark[i].y * image.shape[0]) for i in lightSection4])
    suject5 = np.array([(face_landmarks.landmark[i].x * image.shape[1], face_landmarks.landmark[i].y * image.shape[0]) for i in lightSection5])
    
    mask = np.zeros_like(image)

    colorLight = (130, 70, 20)

    cv2.fillPoly(mask, [suject1.astype(np.int32)], colorLight)
    cv2.fillPoly(mask, [suject2.astype(np.int32)], colorLight)
    cv2.fillPoly(mask, [suject3.astype(np.int32)], colorLight)
    cv2.fillPoly(mask, [suject4.astype(np.int32)], colorLight)
    cv2.fillPoly(mask, [suject5.astype(np.int32)], colorLight)
                
    mask = cv2.GaussianBlur(mask, (39, 39), 0) # Aplicamos un desenfoque gaussiano para suavizar los bordes de la máscar

    image = cv2.addWeighted(image, 1, mask, 0.7, 0)
    
    if 'Ovalado' in face_shape:
        contourSection1 = (345, 436, 432, 367, 345)
        contourSection2 = (116, 216, 212, 138, 116)
    
    elif 'Triangular' in face_shape:
        contourSection1 = (332, 333, 293, 300, 368, 264, 345, 436, 432, 367, 264, 389, 251, 284, 332)
        contourSection2 = (103, 104, 63, 70, 139, 34, 116, 216, 212, 138, 34, 162, 21, 54, 103)
    
    elif 'Rectangular' in face_shape:
        contourSection1 = (345, 436, 416, 367, 434, 430, 394, 379, 365, 397, 288, 366)
        contourSection2 = (116, 216, 192, 138, 214, 210, 169, 150, 136, 172, 58, 137)
    
    else:
        contourSection1 = (0, 0)
        contourSection2 = (0, 0)

    suject7 = np.array([(face_landmarks.landmark[i].x * image.shape[1], face_landmarks.landmark[i].y * image.shape[0]) for i in contourSection2])
    suject6 = np.array([(face_landmarks.landmark[i].x * image.shape[1], face_landmarks.landmark[i].y * image.shape[0]) for i in contourSection1])
    mask2 = np.zeros_like(image)
    colorContour = 255 - 255, 255 - 197, 255 - 229
    cv2.fillPoly(mask2, [suject6.astype(np.int32)], colorContour)
    cv2.fillPoly(mask2, [suject7.astype(np.int32)], colorContour)
    mask2 = cv2.GaussianBlur(mask2, (39, 39), 0) # Aplicamos un desenfoque gaussiano para suavizar los bordes de la máscar
    image = cv2.addWeighted(image, 1, mask2, -0.9, 0)

    return image

@usuarios.route("/revisar_foto", methods=["POST"])
def revisar_foto():
    data = request.get_json()
    imagen_data = data['image']

    # Aquí realizas el procesamiento de la imagen utilizando OpenCV
    imagen_base64 = imagen_data.split(',')[1]  # Eliminar el encabezado 'data:image/jpeg;base64,'
    imagen_bytes = base64.b64decode(imagen_base64)
    nparr = np.frombuffer(imagen_bytes, np.uint8)
    imagen = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    imagen_rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(imagen_rgb)

    # Verificar la orientación de los puntos clave relevantes
    if results.multi_face_landmarks:
        landmarks = results.multi_face_landmarks[0].landmark
        # Calcular los ángulos entre los puntos clave relevantes
        oriented = calcular_angulo(landmarks, imagen)

        if oriented == 1:
            response = { 'Orientado': True }
            return jsonify(response)

    response = { 'Orientado': False }

    return jsonify(response)

def capEyelash(startPoint, endPoint, yPoint, imgSrc, frame, angle):
    # Obtener las coordenadas de los puntos de referencia de la mascara
    start_landmark = startPoint #face_landmarks.landmark[173]
    start_x = int(start_landmark.x * frame.shape[1])
    end_landmark =  endPoint #face_landmarks.landmark[143]
    end_x = int(end_landmark.x * frame.shape[1])

    # Calcular la altura
    height_start = int(yPoint * frame.shape[0]) #face_landmarks.landmark[7].y

    # Imagen a usar
    img = cv2.imread(imgSrc, cv2.IMREAD_UNCHANGED) #'left_eye.png'

    (h, w) = img.shape[:2]
    center = (w / 2, h / 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    img = cv2.warpAffine(img, M, (w, h))

    # Escalar la imagen de las pestañas para que se ajuste al tamaño del ojo
    scale_factor = (start_x - end_x) / img.shape[1]
    img_resized = cv2.resize(img, (0, 0), fx=scale_factor, fy=scale_factor)

    # Superponer la imagen de las pestañas en el frame
    x_offset = end_x
    y_offset = height_start - img_resized.shape[0]
    alpha_s = img_resized[:, :, 3] / 255.0
    alpha_l = 1.0 - alpha_s

    for c in range(0, 3):
        frame[y_offset:y_offset + img_resized.shape[0], x_offset:x_offset + img_resized.shape[1], c] = (
                    alpha_s * img_resized[:, :, c] + alpha_l * frame[
                y_offset:y_offset + img_resized.shape[0],
                x_offset:x_offset + img_resized.shape[1], c])
    
    return frame

def capMakeup(image, landmarks, hexColor, layer = 0, opacity = 0):

    if layer == 0:
        points = (61, 146, 91, 181, 84, 17, 314, 405, 321, 375, 291, 306, 292, 308, 324, 318, 402, 317, 14, 87, 178, 88, 95, 78, 62, 76)
        points2 = (61, 185, 40, 39, 37, 0, 267, 269, 270, 409, 291, 306, 292, 308, 415, 310, 311, 312, 13, 82, 81, 80, 191, 78, 62, 76)
        if opacity == 0:
            opacity = -0.3
        gauss = (5, 5)
    elif layer == 1:
        points = ( 190, 157, 158, 159, 160, 161, 246, 33, 130, 226, 113, 225, 224, 223, 222, 190)
        points2 = ( 414, 384, 385, 386, 387, 388, 466, 263, 359, 446, 342, 445, 444, 443, 442, 414)
        opacity = -0.25
        gauss = (9, 9)

    suject1 = np.array([(landmarks.landmark[i].x * image.shape[1], landmarks.landmark[i].y * image.shape[0]) for i in points])
    suject2 = np.array([(landmarks.landmark[i].x * image.shape[1], landmarks.landmark[i].y * image.shape[0]) for i in points2])

    r, g, b = tuple(int(hexColor[i:i+2], 16) for i in (0, 2, 4))
    r, g, b = 255 - r, 255 - g, 255 - b

    mask = np.zeros_like(image)
    mask2 = np.zeros_like(image)
    color = (b, g, r)
    cv2.fillPoly(mask, [suject1.astype(np.int32)], color)
    cv2.fillPoly(mask2, [suject2.astype(np.int32)], color)

    mask3 = cv2.add(mask, mask2)
    mask3 = cv2.GaussianBlur(mask3, gauss, 0) # Aplicamos un desenfoque gaussiano para suavizar los bordes de la máscara

    result = cv2.addWeighted(image, 1, mask3, opacity, 0)
    return result

@usuarios.route("/procesar", methods=['POST']) # se necesita el atributo link como formato IdLabios:Color,IdPiel:Color,IdPestañas,IdSombras:Color
def procesar_imagen():
    data = request.get_json()
    imagen_data = data['image'] 
    products_data = data['data']
    products = products_data.split(',')

    labialId = products[0].split(':')[0]
    labialColor = products[0].split(':')[1]

    sombrasId = products[3].split(':')[0]
    sombrasColor = products[3].split(':')[1]

    pestañasId = products[2]

    if labialId != '0':
        link = url_for('usuarios.productsApi', _external=True, id = labialId)
        response = requests.get(link).json()
        dataLabial = response['Productos'][0]
        hexLabial = dataLabial['Colores'][labialColor]['Hex']

    if sombrasId != '0':
        link = url_for('usuarios.productsApi', _external=True, id = sombrasId)
        response = requests.get(link).json()
        dataSombras = response['Productos'][0]
        hexSombras = dataSombras['Colores'][sombrasColor]['Hex']

    # Aquí realizas el procesamiento de la imagen utilizando OpenCV
    imagen_base64 = imagen_data.split(',')[1]  # Eliminar el encabezado 'data:image/jpeg;base64,'
    imagen_bytes = base64.b64decode(imagen_base64)
    nparr = np.frombuffer(imagen_bytes, np.uint8)
    imagen = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Procesar la imagen para poner el maquillaje
    imagen_rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(imagen_rgb)

    if results.multi_face_landmarks:
        face_landmarks = results.multi_face_landmarks[0]
        if labialId != '0':
            imagen = capMakeup(imagen, face_landmarks, hexLabial, 0, -0.25)
            
        if sombrasId != '0':
            imagen = capMakeup(imagen, face_landmarks, hexSombras, 1)

        if pestañasId != '0':
            imagen = capEyelash(face_landmarks.landmark[173], face_landmarks.landmark[143], face_landmarks.landmark[7].y, 'static/img/left_eye.png', imagen, angle=0)
            imagen = capEyelash(face_landmarks.landmark[372], face_landmarks.landmark[398], face_landmarks.landmark[249].y, 'static/img/right_eye.png', imagen, angle=0)
        

    # Convertir la imagen procesada de nuevo a base64
    _, imagen_procesada_encoded = cv2.imencode('.jpeg', imagen)
    imagen_procesada_base64 = base64.b64encode(imagen_procesada_encoded).decode('utf-8')

    # Construir la respuesta con la imagen procesada
    response = {
        'processedImageUrl': imagen_procesada_base64
    }
    return jsonify(response)

@usuarios.route("/procesarRostro", methods=['POST'])
def processShape():
    data = request.get_json()
    imagen_data = data['image']

    imagen_base64 = imagen_data.split(',')[1]  # Eliminar el encabezado 'data:image/jpeg;base64,'
    imagen_bytes = base64.b64decode(imagen_base64)
    nparr = np.frombuffer(imagen_bytes, np.uint8)
    imagen = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Procesar la imagen para poner el maquillaje
    imagen_rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(imagen_rgb)

    if results.multi_face_landmarks:
        face_landmarks = results.multi_face_landmarks[0]
        face_shape = detectFaceShape(face_landmarks)
        imagen = waysToMakeup(face_landmarks, imagen)

    # Convertir la imagen procesada de nuevo a base64
    _, imagen_procesada_encoded = cv2.imencode('.jpeg', imagen)
    imagen_procesada_base64 = base64.b64encode(imagen_procesada_encoded).decode('utf-8')

    response = {
        'Forma': face_shape,
        'processedImageUrl': imagen_procesada_base64
    }

    return jsonify(response)


def numeroorden(id):
    subject = 'Pedido Realizado con éxito'
    sender = "decore.makeup.soporte@gmail.com"
    with mysql.connect.cursor() as cursor:
        cursor.execute("SELECT MAX(ordenpago.Id_Orden) AS Orden, cuenta.Correo FROM cuenta INNER JOIN usuarios ON cuenta.Id_Cuenta = usuarios.Id_Usuario INNER JOIN ordenpago ON usuarios.Id_Usuario = ordenpago.Id_Usuario WHERE cuenta.Id_Cuenta = %s GROUP BY cuenta.Correo", (id,))
        resultado = cursor.fetchone()
    message = Message(subject, sender=sender, recipients=[resultado[1]])
    message.body = f"Estimado Cliente,\n\nSe ha realizado su pedido correctamente. Su número de orden es:\n\n{resultado[0]}\n\nSaludos,\nEquipo de Decore"
    mail.send(message)


def actualizar_promedios():
    with mysql.connect.cursor() as cursor:
        cursor.execute("SELECT Id_producto, AVG(Calificacion) AS PromedioCalificacion FROM Foro GROUP BY Id_producto")
        resultados = cursor.fetchall()

        for resultado in resultados:
            id_producto = resultado[0]
            promedio_calificacion = resultado[1]
            with mysql.connection.cursor() as cursor:
                cursor.execute("UPDATE recomendacion SET Promedio_Calificacion = %s WHERE Id_Producto = %s", (promedio_calificacion, id_producto))
                mysql.connection.commit()


@usuarios.route("/tasks")
@usuarios.route("/tasks/<string:starter>", methods=['GET', 'POST'])
def tasks(starter = ""):
    return render_template("usuarios/cam.jinja", starter = starter)
def tasks():
    return render_template("usuarios/cam.jinja")

def actualizaredad(id):
    with mysql.connect.cursor() as cursor:
        # Obtener la orden de pago con el Id_Orden más grande
        cursor.execute(" SELECT usuarios.Edad, ordenpago.carrito FROM usuarios INNER JOIN ordenpago ON ORDENPAGO.Id_Usuario = usuarios.Id_Usuario WHERE ordenpago.Id_Usuario = %s ORDER BY ordenpago.Id_Orden DESC LIMIT 1", (id,))
        result = cursor.fetchone()

        if result:
            carrito = result[1].split("|")  # Separar los valores por el carácter "|"
            edad = int(result[0])  # Obtener la edad del usuario
            
            with mysql.connection.cursor() as cursor:
                for item in carrito:
                    values = item.split(",")  # Separar los valores por el carácter ","
                    producto_id = int(values[0])  # Obtener el primer dígito (Id_Producto)
                    print(edad)
                    print(producto_id)
                    cursor.execute("UPDATE recomendacion SET Promedio_Edad = (Promedio_Edad + %s), NumVentas = (NumVentas+1) WHERE Id_Producto = %s", (edad, producto_id))
                mysql.connection.commit()

@usuarios.route('/actualizarvistas', methods=['POST'])
def actualizar_vistas():
    productoid = request.form.get('productoid')
    
    with mysql.connection.cursor() as cursor:
            cursor.execute("UPDATE recomendacion SET Promedio_Vistas = (Promedio_Vistas + 1) WHERE Id_Producto = %s", (productoid,))
            mysql.connection.commit()

    return jsonify({'success': True})

@usuarios.route("/productsApiordenar")
@usuarios.route("/productsApiordenar/<string:id>?<string:idUsuario>", methods=['GET'])
def productsApiordenar(id=0, idUsuario = 0):
    keys = [
    'Id',
    'Nombre', 
    'Imagenes',
    'Descripcion',
    'Precio u.',
    'Nombre color',
    'Hex color',
    'Categoria',
    'Recomendacion',
    'Marca',
    'Stock',
    'Tipo de piel',
    'Imagenes filtro',
    'Tipo'
    ]
    
    arr = []
    colors = {}


    with mysql.connect.cursor() as cursor:
        if id == "1":
            cursor.execute("""SELECT productos.* FROM productos 
            inner join 
                recomendacion on productos.Id_productos = recomendacion.Id_Producto 
            order by NumVentas DESC Limit 10""")

        elif id == "2":
            cursor.execute("""SELECT productos.* FROM productos 
            inner join 
                recomendacion on productos.Id_productos = recomendacion.Id_Producto 
            order by Promedio_Vistas DESC Limit 10""")

        elif id == "3":
            profileInfo = takeProfileInfo(idUsuario)
            cursor.execute("SELECT Hex FROM color_ojos WHERE Id_ColorOjos = %s", (profileInfo[3],))
            coloresOjos = cursor.fetchone()
            cursor.execute("SELECT productos.* FROM productos INNER JOIN recomendacion ON productos.Id_Productos = recomendacion.Id_Producto ORDER BY CASE WHEN recomendacion.Color_Ojos LIKE %s THEN 1 ELSE 2 END, CASE WHEN recomendacion.Color_Pelo LIKE %s THEN 1 ELSE 2 END, CASE WHEN recomendacion.Color_Piel LIKE %s THEN 1 ELSE 2 END, CASE WHEN recomendacion.Promedio_Edad BETWEEN %s AND %s THEN 1 ELSE 2 END;", ("%" + str(coloresOjos[0]) + "%", "%" + str(profileInfo[6]) + "%", "%" + str(profileInfo[5]) + "%", int(profileInfo[2]) - 3, int(profileInfo[2]) + 3))
        rows = cursor.fetchall()
        for item in rows:
            ord = OrderedDict(zip(keys, item))
            # Dividir los nombres de colores y los valores de Hex
            color_names = ord['Nombre color'].split(',')
            hex_values = ord['Hex color'].split(',')

            # Crear un nuevo JSON para cada color
            colors = {}
            for i, name in enumerate(color_names):
                colors[i+1] = {'Nombre': name, 'Hex': hex_values[i]}

            # Reemplazar 'Nombre color' y 'Hex color' con el nuevo JSON
            ord['Colores'] = colors
            del ord['Nombre color']
            del ord['Hex color']

            arr.append(ord)

    response = make_response(jsonify({
            'Productos': arr
        }), 200)

    response.headers["Content-type"] = "application/json"
    return response