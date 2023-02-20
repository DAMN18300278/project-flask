from flask_mysqldb import MySQL
from flask import render_template, session, redirect, flash, Blueprint

empleados = Blueprint('empleados', __name__)
mysql = MySQL()

@empleados.record_once
def on_load(state):
    app = state.app
    mysql.init_app(app)

def asignarNombre(idEmpleado):
    with mysql.connect.cursor() as cursor:
        cursor.execute('SELECT Nombre_Empleado FROM empleado WHERE Id_Empleado = %s', (idEmpleado,))
        rows = cursor.fetchall()
        
        for row in rows:
            nombre = row['Nombre_Empleado']  
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
    with mysql.connect.cursor() as cursor:
        cursor.execute("SELECT empleado.Id_Empleado, empleado.Nombre_Empleado, tipo_empleado.Tipo FROM empleado INNER JOIN tipo_empleado ON empleado.Tipo_Empleado = tipo_empleado.Id_Tipo")
        resultado = cursor.fetchall()
    print(resultado)
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