import flask
import requests
from flask import session, render_template, redirect, jsonify, make_response, url_for, request
from flask_mysqldb import MySQL
from collections import OrderedDict

usuarios = flask.Blueprint('usuarios', __name__)
mysql = MySQL()

@usuarios.record_once
def on_load(state):
    app = state.app
    mysql.init_app(app)

@usuarios.route("/productsApi")
@usuarios.route("/productsApi/<id>", methods=['GET'])
def productsApi(id = 0):
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

    return render_template("usuarios/landing.jinja", productos = data)

@usuarios.route("/usuarios/delete")
def delete():
    session.clear()
    return redirect("/")