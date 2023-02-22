from flask_mysqldb import MySQL
from flask import render_template, session, redirect, flash, Blueprint
from flask import request

empleados = Blueprint('empleados', __name__)
mysql = MySQL()

@empleados.record_once
def on_load(state):
    app = state.app
    mysql.init_app(app)

def asignarNombre(idEmpleado):
    with mysql.connect.cursor() as cursor:
        cursor.execute('SELECT Nombre_Empleado FROM empleado WHERE Id_Empleado = %s', (idEmpleado,))
        rows = cursor.fetchone()
        print(rows)
        nombre = rows[0]  
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
        cursor.execute("SELECT empleado.Id_Empleado, empleado.Nombre_Empleado, `tipo empleado`.Tipo FROM empleado INNER JOIN `tipo empleado` ON empleado.Tipo_Empleado = `tipo empleado`.Id_Tipo")
        resultado = cursor.fetchall()

    return render_template("empleados/EmpleadosList.jinja", resultados = resultado)

@empleados.route('/administradores/editarEmpleados/<id>', methods=['POST', 'GET'])
def Admin_empleados_Edit(id):
    with mysql.connect.cursor() as cursor:

        cursor.execute("SELECT empleado.Nombre_Empleado, cuenta.Correo, cuenta.Contraseña ,empleado.RFC, empleado.Direccion, empleado.RFC, empleado.Tipo_Empleado FROM empleado INNER JOIN cuenta ON cuenta.Id_cuenta = empleado.Id_Empleado WHERE cuenta.Id_cuenta = %s", id)
        resultado = cursor.fetchone()
    
    print(resultado)
    return render_template("empleados/EmpEdit.jinja", empleado = resultado)

@empleados.route('/administradores/BorrarEmpleados/<id>')
def Admin_empleados_Delete(id):
    return redirect("/")


@empleados.route("/administradores/OrdenesPago")
def PagosAdmin():
    return render_template("empleados/OrdenesPago.jinja")

@empleados.route("/administradores/GuardarEmp/<id>", methods=['POST','GET'])
def GuardarEmp(id):
    
    nombre = request.form['EmpNombre']
    email = request.form['EmpEmail']
    password = request.form['EmpPassword']
    rfc = request.form['EmpRFC']
    direccion = request.form['EmpDireccion']
    tipo = request.form['listaTipo']
    with mysql.connect.cursor() as cursor:
        cursor.execute("UPDATE cuenta SET Correo = %s , Contraseña = %s WHERE Id_cuenta = %s", (email, password ,id))
        
    return redirect("/administradores/EmpleadosList")

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