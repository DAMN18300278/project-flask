import flask
import requests
from flask import session, render_template, redirect, jsonify, make_response, url_for, request
from flask_mysqldb import MySQL
from collections import OrderedDict
import base64
import cv2
import numpy as np

usuarios = flask.Blueprint('usuarios', __name__)
mysql = MySQL()

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
    return render_template("usuarios/landing.jinja", productos = data, idUsuario = session.get('id_usuario'), carrito = numero)

@usuarios.route("/usuarios/addcarrito", methods=['POST'])
def addcarrito():
    carritoData = request.form['carritoData']
    idUsuario = request.form['id']
    with mysql.connection.cursor() as cursor:
        cursor.execute("UPDATE usuarios SET Carrito = CONCAT(Carrito, %s) WHERE id_Usuario = %s", (carritoData, idUsuario))
        mysql.connection.commit()
        cursor.close()
    return redirect("/")

@usuarios.route('/usuarios/eliminar_producto/<string:id>', methods=['POST'])
def eliminar_producto(id):
    ids = id.split('_')
    id_producto = int(ids[0])-1
    id = ids[1]
    with mysql.connect.cursor() as cursor:
        cursor.execute("SELECT Carrito FROM usuarios WHERE Id_Usuario = %s",id,)
        fetch = cursor.fetchone()
        carrito = fetch[0].split('|')[1:] 
        del carrito[id_producto]
        carrito_str = '|'.join(carrito)
        carrito_str = "|"+carrito_str
    with mysql.connection.cursor() as cursor:
        cursor.execute("UPDATE usuarios SET Carrito = %s WHERE id_Usuario = %s", (carrito_str, id))
        mysql.connection.commit()
        cursor.close()
    return 'OK'

@usuarios.route("/usuarios/ordencarrito/<string:id>", methods=['POST','GET'])
def ordencarrito(id):

    with mysql.connect.cursor() as cursor:
        
        cursor.execute("SELECT Carrito FROM usuarios WHERE Id_Usuario = %s",id,)
        fetch = cursor.fetchone()
        if not fetch or not fetch[0]:
            numero = 0
            productos = []
        else:
            
            carrito = fetch[0].split('|')[1:] # se elimina el primer elemento vacío de la lista
            
            numero = len(carrito)
            productos = []
            i = 0
            for producto in carrito:
                producto = producto.split(',')
                productos.append(producto)

                cursor.execute("SELECT Color_RGBA FROM productos WHERE Id_Productos = %s",producto[0],)
                color = cursor.fetchone()[0].split(',')

                producto[2] = int(producto[2])
                indice_color = int(producto[2])-1

                productos[i].append(color[indice_color])

                #print(color[int(productos[int(productos[i][2])])])
                cursor.execute("SELECT Nombre,Precio FROM productos WHERE Id_Productos = %s",productos[i][0],)
                datos = cursor.fetchone()
                
                productos[i].extend(datos)
                
                i+=1
        cursor.execute("SELECT Nombre FROM usuarios WHERE Id_Usuario = %s",id,)    
        nombre = cursor.fetchone()[0]
        
    return render_template("usuarios/CarritoCompras.jinja",id=id,numero = numero,productos=productos, nombre=nombre)


@usuarios.route("/cam")
def cam():
    return render_template("usuarios/cam.jinja")

@usuarios.route('/cam2', methods=['POST'])
def upload():
  # Obtener la imagen como un objeto base64
  data = request.get_json()
  image = data['image']
  # Decodificar la imagen de base64
  imgdata = base64.b64decode(image.split(',')[1])
  # Convertir la imagen en un array de numpy
  nparr = np.frombuffer(imgdata, np.uint8)
  img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
  # Aplicar un filtro a la imagen
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  cv2.imshow('prueba', gray)
  # Convertir la imagen de nuevo en base64
  retval, buffer = cv2.imencode('.jpg', gray)
  gray_base64 = base64.b64encode(buffer).decode('utf-8')
  # Devolver la imagen procesada como una respuesta HTTP en formato JSON
  return jsonify(image=gray_base64)