import flask
import pymysql
from flask import render_template, session, redirect, flash

empleados = flask.Blueprint('empleados', __name__)

def connection():
    return pymysql.connect(host='localhost',
                                user='root',
                                password='',
                                db='diegomedel$decore')

@empleados.route("/administradores")
def indexAdmin():
    conexion = connection()

    with conexion.cursor() as cursor:
        cursor.execute("SELECT Nombre_Empleado FROM empleado WHERE Id_Empleado = %s", session['id_administrador'])
        rows = cursor.fetchall()
        
        for row in rows:
            flash(f'{row[0]}')
            
    return render_template("empleados/indexAdmin.html")

@empleados.route("/administradores/delete")
def delAdmin():
    session.clear()
    return redirect("/")

@empleados.route("/caja")
def indexCaja():
    return render_template("empleados/indexCaja.html")

@empleados.route("/supervisores")
def indexSupervisor():
    return render_template("empleados/indexSupervisores.html")

@empleados.route("/inventario")
def indexInv():
    return render_template("empleados/indexAlmacen.html")