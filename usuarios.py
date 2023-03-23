import flask
import json
from flask import session, render_template, redirect, jsonify, make_response
from flask_mysqldb import MySQL

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
    'Rgba color',
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
            ord = dict(zip(keys, rows))
            arr.append(ord)
        else:
            cursor.execute("SELECT * FROM productos")
            rows = cursor.fetchall()
            for item in rows:
                # item[2] = json.dumps(item[2].split(","))
                # item[5] = item[5].split(", ")
                # item[6] = item[6].split("|")
                values = []
                values = item
                pua = json.dumps(item[5].split(","))
                puaa = json.dumps(item[6].split("|")) 
                print(type(pua))
                ord = dict(zip(keys, pua))
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