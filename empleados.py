import flask
import pymysql
from flask import render_template, session, redirect, flash

empleados = flask.Blueprint('empleados', __name__)

def connection():
    return pymysql.connect(host='localhost',
                                user='root',
                                password='',
                                db='diegomedel$decore')

def asignarNombre(idEmpleado):
    conexion = connection()

    with conexion.cursor() as cursor:
        cursor.execute("SELECT Nombre_Empleado FROM empleado WHERE Id_Empleado = %s", idEmpleado)
        rows = cursor.fetchall()
        
        for row in rows:
            nombre = row[0]  
        flash(nombre[:(nombre.index(' '))])

@empleados.route("/administradores")
def indexAdmin():
    asignarNombre(session['id_administrador'])
    return render_template("empleados/indexAdmin.jinja")

@empleados.route("/administradores/inventario")
def invAdmin():
    return render_template("empleados/inventario.jinja")

@empleados.route("/administradores/EmpleadosList")
def EmpAdmin():
    conexion = connection()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT empleado.Id_Empleado, empleado.Nombre_Empleado, tipo_empleado.Tipo FROM empleado INNER JOIN tipo_empleado ON empleado.Tipo_Empleado = tipo_empleado.Id_Tipo;")
        resultado = cursor.fetchall()
    return render_template("empleados/EmpleadosList.jinja", resultados = resultado)

@empleados.route("/administradores/OrdenesPago")
def PagosAdmin():
    return render_template("empleados/OrdenesPago.jinja")

@empleados.route("/administradores/delete")
def delAdmin():
    session.clear()
    return redirect("/")

@empleados.route("/caja")
def indexCaja():
    asignarNombre(session['id_encargadoCaja'])
    return render_template("empleados/indexCaja.jinja")

@empleados.route("/supervisores")
def indexSupervisor():
    asignarNombre(session['id_supervisor'])
    return render_template("empleados/indexSupervisores.jinja")

@empleados.route("/inventario")
def indexInv():
    asignarNombre(session['id_inventario'])
    return render_template("empleados/indexAlmacen.jinja")