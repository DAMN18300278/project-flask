import flask
from flask import session, render_template, redirect

usuarios = flask.Blueprint('usuarios', __name__)

@usuarios.route("/usuarios/index")
def index():
    return render_template("usuarios/landing.jinja")

@usuarios.route("/usuarios/delete")
def delete():
    session.clear()
    return redirect("/")