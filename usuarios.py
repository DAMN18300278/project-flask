import flask
import requests
from flask import session, render_template, redirect, jsonify, make_response, url_for, request, flash, Response
from flask_mysqldb import MySQL
from collections import OrderedDict
import base64
from datetime import datetime
import cv2
import numpy as np
import base64
import mediapipe as mp
import math

usuarios = flask.Blueprint('usuarios', __name__)
mysql = MySQL()

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

    with mysql.connect.cursor() as cursor:
        cursor.execute("SELECT Carrito FROM usuarios WHERE Id_Usuario = %s", (session.get('id_usuario'),))
        fetch = cursor.fetchone()
        if fetch is None or not fetch[0]:
            numero = 0
        else:
            abubu = fetch[0].split("|")
            numero = len(abubu)

    
    return render_template("usuarios/landing.jinja", productos = data, idUsuario = session.get('id_usuario'), carrito = numero,nombre = nombre)


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
                
                print(carrito)
                numero = len(carrito)
                
                i = 0
                for producto in carrito:
                    producto = producto.split(',')
                    productos.append(producto)
                    print(producto[0])
                    print(producto[1])
                    with mysql.connect.cursor() as cursor:
                        cursor.execute("SELECT Cantidad From productos where Id_Productos = %s",(producto[0],))
                        cantidad = int(cursor.fetchone()[0])
                        print(cantidad)
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
        print(forum[0][4])

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
    
    return redirect("/")

def takeProfileInfo():
    with mysql.connect.cursor() as cursor:
        cursor.execute("SELECT * FROM usuarios WHERE Id_Usuario = %s", (session.get("id_usuario"),))
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
    colorCabello = request.form["colorCabello"]
    with mysql.connection.cursor() as cursor:
        cursor.execute("UPDATE usuarios SET Nombre = %s, Edad = %s, Color_Ojos = %s, Tipo_Piel = %s, Tono_Piel = %s, Color_Pelo = %s WHERE Id_Usuario = %s",
                       (nombre, edad, colorOjos, tipoPiel, colorPiel, colorCabello, session.get('id_usuario')))
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

def capMakeup(image, landmarks, hexColor, layer = 0):

    if layer == 0:
        points = (61, 146, 91, 181, 84, 17, 314, 405, 321, 375, 291, 306, 292, 308, 324, 318, 402, 317, 14, 87, 178, 88, 95, 78, 62, 76)
        points2 = (61, 185, 40, 39, 37, 0, 267, 269, 270, 409, 291, 306, 292, 308, 415, 310, 311, 312, 13, 82, 81, 80, 191, 78, 62, 76)
        opacity = -0.5
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
    mask3 = cv2.GaussianBlur(mask3, gauss, 0) # Aplicamos un desenfoque gaussiano para suavizar los bordes de la máscar
    cv2.imshow('prueba', mask3)

    result = cv2.addWeighted(image, 1, mask3, opacity, 0)
    
    return result

@usuarios.route("/procesar", methods=['POST'])
def procesar_imagen():
    data = request.get_json()
    imagen_data = data['image'] 

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

        imagen = capMakeup(imagen, face_landmarks, 'eb6369', 1)
        imagen = capMakeup(imagen, face_landmarks, 'bc0f28', 0)

    # Convertir la imagen procesada de nuevo a base64
    _, imagen_procesada_encoded = cv2.imencode('.jpeg', imagen)
    imagen_procesada_base64 = base64.b64encode(imagen_procesada_encoded).decode('utf-8')

    # Construir la respuesta con la imagen procesada
    response = {
        'processedImageUrl': imagen_procesada_base64
    }
    
    return jsonify(response)

@usuarios.route("/tasks")
def tasks():
    return render_template("usuarios/cam.jinja")