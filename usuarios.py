import flask
from flask import session, render_template, redirect
from flask_mysqldb import MySQL

usuarios = flask.Blueprint('usuarios', __name__)
mysql = MySQL()

@usuarios.record_once
def on_load(state):
    app = state.app
    mysql.init_app(app)

@usuarios.route("/usuarios")
def index():
    with mysql.connect.cursor() as cursor:
        cursor.execute('SELECT * FROM productos')

    return render_template("usuarios/landing.jinja")

@usuarios.route("/usuarios/delete")
def delete():
    session.clear()
    return redirect("/")