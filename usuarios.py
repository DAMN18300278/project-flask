import flask
import json
from flask import session, render_template, redirect, jsonify, make_response
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
def productsApi(id=0):
    keys = [
        'Id',
        'Nombre',
        'Imagenes',
        'Descripcion',
        'Precio u.',
        'Nombre color',
        'Rgba color',
        'Categoria',
        'Recomendacion',
        'Marca',
        'Stock',
        'Tipo de piel',
        'Imagenes filtro'
    ]
   
    new_keys = [
        'Id',
        'Nombre',
        'Imagenes',
        'Descripcion',
        'Precio u.',
        'Colores',
        'Categoria',
        'Recomendacion',
       
        'Marca',
        'Stock',
        'Tipo de piel',
        'Imagenes filtro'
    ]
    arr = []
    with mysql.connect.cursor() as cursor:
        if id != 0:
            cursor.execute("SELECT * FROM productos WHERE Id_Productos = %s", (id,))
            rows = cursor.fetchone()
            ord = OrderedDict(zip(keys, rows))
            arr.append(ord)
        else:
            cursor.execute("SELECT * FROM productos")
            rows = cursor.fetchall()
            for item in rows:
                ord = OrderedDict(zip(keys, item))
                # Dividir los nombres de colores y los valores de RGBA
                color_names = ord['Nombre color'].split(',')
                rgba_values = ord['Rgba color'].split('|')
                # Crear un nuevo JSON para cada color
                colors = {}
                for i, name in enumerate(color_names):
                    colors[name] = {'Nombre': name, 'Rgba': rgba_values[i]}
                # Reemplazar 'Nombre color' y 'Rgba color' con el nuevo JSON
                ord['Colores'] = colors
                del ord['Nombre color']
                del ord['Rgba color']
                # Reordenar el JSON según el nuevo orden de keys
                ord = OrderedDict((k, ord[k]) for k in new_keys)
                arr.append(ord)
                response = make_response(jsonify({
                    'Productos': arr
                }), 200)
    response.headers["Content-type"] = "application/json"
    return response

@usuarios.route("/usuarios")
def index():
    return render_template("usuarios/landing.jinja")

@usuarios.route("/usuarios/delete")
def delete():
    session.clear()
    return redirect("/")