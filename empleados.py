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
    return render_template("empleados/indexAdmin.html")

@empleados.route("/administradores/inventario")
def InvAdmin():
    flash("administrador")
    
    return render_template("empleados/indexAdmin.html")

@empleados.route("/administradores/delete")
def delAdmin():
    session.clear()
    return redirect("/")

@empleados.route("/caja")
def indexCaja():
    asignarNombre(session['id_encargadoCaja'])
    return render_template("empleados/indexCaja.html")

@empleados.route("/supervisores")
def indexSupervisor():
    asignarNombre(session['id_supervisor'])
    return render_template("empleados/indexSupervisores.html")

@empleados.route("/inventario")
def indexInv():
    asignarNombre(session['id_inventario'])
    return render_template("empleados/indexAlmacen.html")

@empleados.route("/mostrarempelados")
def mostEmp():
    conexion = connection()
    with conexion.cursor() as cursor:
        cursor.execute("Select empleado.Id_Empleado, empleado.Nombre_Empleado, tipo_empleado.Tipo from empleado INNER JOIN tipo_empleado ON empleado.Id_Empleado = tipo_empleado.Id_Tipo")
        resultado = cursor.fetchall()
        return render_template("/EmpleadosList.html", resultado = resultado)
