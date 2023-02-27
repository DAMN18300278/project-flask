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
    with mysql.connect.cursor() as cursor:
        cursor.execute("SELECT Id_Productos, Nombre, Cantidad From productos")
        resultado = cursor.fetchall()
    return render_template("empleados/inventario.jinja", resultados = resultado)

@empleados.route("/administradores/EmpleadosList")
def EmpAdmin():
    with mysql.connect.cursor() as cursor:
        cursor.execute("SELECT empleado.Id_Empleado, empleado.Nombre_Empleado, tipo_empleado.Tipo FROM empleado INNER JOIN tipo_empleado ON empleado.Tipo_Empleado = tipo_empleado.Id_Tipo ORDER BY empleado.Id_Empleado ASC")
        resultado = cursor.fetchall()

    return render_template("empleados/EmpleadosList.jinja", resultados = resultado)

@empleados.route('/administradores/editarEmpleados', methods=['POST', 'GET'])
@empleados.route('/administradores/editarEmpleados/<id>', methods=['POST', 'GET'])
def Admin_empleados_Edit(id=None):
    if id:
        with mysql.connection.cursor() as cursor:
            cursor.execute("SELECT empleado.Nombre_Empleado, cuenta.Correo, cuenta.Contraseña ,empleado.RFC, empleado.Direccion, empleado.RFC, empleado.Tipo_Empleado, empleado.Id_Empleado FROM empleado INNER JOIN cuenta ON cuenta.Id_cuenta = empleado.Id_Empleado WHERE cuenta.Id_cuenta = %s", id)
            resultado = cursor.fetchone()
        return render_template("empleados/EmpEdit.jinja", empleado = resultado)
    else:
        return render_template("empleados/EmpEdit.jinja", empleado = "")

@empleados.route('/administradores/BorrarEmpleados/<int:id>')
def Admin_empleados_Delete(id):

    with mysql.connection.cursor() as cursor:
        
        cursor.execute("DELETE FROM empleado WHERE Id_Empleado = %s", (id,))
        mysql.connection.commit()
        cursor.execute("DELETE FROM cuenta WHERE Id_cuenta = %s", (id,))
        mysql.connection.commit()

    return redirect("/administradores/EmpleadosList")


@empleados.route("/administradores/OrdenesPago")
def PagosAdmin():

    with mysql.connect.cursor() as cursor:
        cursor.execute("SELECT OrdenPago.Id_Orden,usuarios.Nombre ,OrdenPago.Fecha FROM OrdenPago INNER JOIN usuarios ON usuarios.Id_Usuario = OrdenPago.Id_Usuario ORDER BY Id_Orden ASC")
        resultado = cursor.fetchall()
    return render_template("empleados/OrdenesPago.jinja", resultados = resultado)

@empleados.route("/administradores/OrdenEspecifica/<int:id>")
def OrdenUsuario(id):

    return render_template("empleados/OrdenEspecifica.jinja",id=id)

@empleados.route("/administradores/GuardarEmp", methods=['POST', 'GET'])
@empleados.route("/administradores/GuardarEmp/<int:id>", methods=['POST','GET'])
def GuardarEmp(id=None):
    nombre = request.form['EmpNombre']
    email = request.form['EmpEmail']
    password = request.form['EmpPassword']
    tel = request.form['EmpTelefono']
    rfc = request.form['EmpRFC']
    direccion = request.form['EmpDireccion']
    tipo = request.form['ListaTipo']
    if id:
        
        with mysql.connection.cursor() as cursor:
            cursor.execute("UPDATE cuenta SET Correo = %s, Contraseña = %s WHERE Id_cuenta = %s", (email, password, id))
            mysql.connection.commit()
            cursor.execute("UPDATE empleado SET RFC = %s, Nombre_Empleado = %s, Telefono = %s, Direccion = %s, Tipo_Empleado = %s WHERE Id_Empleado = %s",(rfc, nombre, tel, direccion, tipo, id))
            mysql.connection.commit()
        return redirect("/administradores/EmpleadosList")
    else:
        with mysql.connection.cursor() as cursor:
            cursor.execute("SELECT MAX(Id_cuenta) FROM cuenta")
            max_id = cursor.fetchone()[0] or 0 # esta linea es para obtener el primer valor y verifique que no se encuentre vacia
            print(max_id)
            #Insertar en la tabla cuenta con el id máximo + 1
            cursor.execute("INSERT INTO cuenta(Id_cuenta, Rol, Correo, Contraseña, estado) VALUES (%s, %s, %s, %s, %s)", (max_id + 1, tipo, email, password, 'Inactivo'))
            mysql.connection.commit()
            # Insertar en la tabla empleado con el mismo id_cuenta
            cursor.execute("INSERT INTO empleado(Id_Empleado, RFC, Nombre_Empleado, Telefono, Direccion, Tipo_Empleado) VALUES (%s, %s, %s, %s, %s, %s)", (max_id + 1, rfc, nombre, tel, direccion, tipo))
            mysql.connection.commit()
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