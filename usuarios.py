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
        cursor.execute("SELECT Carrito FROM Usuarios WHERE Id_Usuario = %s", (session.get('id_usuario'),))
        fetch = cursor.fetchone()
        if not fetch[0]:
            carrito = list()

    return render_template("usuarios/landing.jinja", productos = data, idUsuario = session.get('id_usuario'), carrito = carrito)

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