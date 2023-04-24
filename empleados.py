from flask_mysqldb import MySQL
from flask import render_template, session, redirect, flash, Blueprint, request, url_for

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
        nombre = rows[0]  
        flash(nombre[:(nombre.index(' '))])

@empleados.route("/administradores")
def indexAdmin():
    asignarNombre(session['id_administrador'])
    return render_template("empleados/indexAdmin.jinja")

@empleados.route("/administradores/inventario/Agregar")
def Agregar():
    return render_template("empleados/inventarioNewProd.jinja")

@empleados.route("/administradores/inventario")
def invAdmin():
    with mysql.connect.cursor() as cursor:
        cursor.execute("SELECT Id_Productos, Nombre, Cantidad From productos")
        resultado = cursor.fetchall()
    return render_template("empleados/inventario.jinja" , resultados = resultado)

@empleados.route("/administradores/inventario/<int:id>", methods=['POST', 'GET'])
def UpCantidad(id):
    cantidad = request.form['cantidad']
    with mysql.connection.cursor() as cursor:
        cursor.execute("Update productos SET Cantidad = %s where %s = Id_Productos",(cantidad, id))
        mysql.connection.commit()
    return redirect("/administradores/inventario")

@empleados.route("/administradores/inventario/NuevoProducto", methods=['POST','GET'])
def añadir_producto():
    if request.method == 'POST':
        id_producto = request.form['IdProducto']
        nombre = request.form['Nombre']
        imagen = request.files.getlist('Imagen[]')
        num_imagenes = len(imagen)
        descripcion = request.form['Descripcion']
        precio = request.form['Precio']
        
        nombre_color = request.form.getlist('nombre_color') # Obtener la lista de nombres de colores
        color_rgba = request.form.getlist('color') # Obtener la lista de valores hexadecimales de colores
        # Convertir las listas en strings separados por comas
        nombre_color = ','.join(nombre_color)
        color_rgba = ','.join(color_rgba)
       
        categoria = request.form['Categoria']
        cantidad = request.form['Cantidad']
        marca = request.form['Marca']
        tipo_piel = request.form['TipoPiel']
        recomendacion = request.form['Recomendacion']
        imagen_filtro = request.files.getlist('Imagen_fil[]')
        filtronames = ','.join([file.filename for file in imagen_filtro])

    with mysql.connection.cursor() as cursor:
            cursor.execute("INSERT INTO productos(Id_Productos, Nombre, Imagen, Descripcion, Precio, Nombre_Color, Color_RGBA, Categoria, Recomendacion, Marca, Cantidad , Tipo_Piel, Imagen_filtro) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)", (id_producto, nombre,num_imagenes, descripcion, precio, nombre_color, color_rgba, categoria, recomendacion, marca, cantidad, tipo_piel,filtronames))
            mysql.connection.commit()
    return redirect("/administradores/inventario")


@empleados.route("/administradores/EmpleadosList")
def EmpAdmin():
    with mysql.connect.cursor() as cursor:
        cursor.execute("SELECT empleado.Id_Empleado, empleado.Nombre_Empleado, tipo_empleado.Tipo FROM empleado INNER JOIN tipo_empleado ON empleado.Tipo_Empleado = tipo_empleado.Id_Tipo ORDER BY empleado.Id_Empleado ASC")
        resultado = cursor.fetchall()
    return render_template("empleados/EmpleadosList.jinja", resultados = resultado)

@empleados.route('/administradores/editarEmpleados', methods=['POST', 'GET'])
@empleados.route('/administradores/editarEmpleados/<int:id>', methods=['POST', 'GET'])
def Admin_empleados_Edit(id=None):
    if id:
        with mysql.connect.cursor() as cursor:
            cursor.execute("SELECT empleado.Nombre_Empleado, cuenta.Correo, cuenta.Contraseña ,empleado.RFC, empleado.Direccion, empleado.RFC, empleado.Tipo_Empleado, empleado.Id_Empleado FROM empleado INNER JOIN cuenta ON cuenta.Id_cuenta = empleado.Id_Empleado WHERE cuenta.Id_cuenta = %s", (id,))
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
        cursor.execute("SELECT OrdenPago.Id_Orden,usuarios.Nombre ,OrdenPago.Fecha, OrdenPago.Status, OrdenPago.Id_Usuario FROM OrdenPago INNER JOIN usuarios ON usuarios.Id_Usuario = OrdenPago.Id_Usuario ORDER BY Id_Orden ASC")
        resultado = cursor.fetchall()
    return render_template("empleados/OrdenesPago.jinja", resultados = resultado)



@empleados.route("/administradores/OrdenEspecifica/RecogerCaja/<string:id>")
def RecogerCaja(id):
    with mysql.connection.cursor() as cursor:
        cursor.execute("INSERT INTO ordenpago(Id_Orden, Id_Usuario, Fecha, Status) VALUES (NULL, %s, NOW(), 'Pagar en caja')", (id,))
        mysql.connection.commit()
    return redirect("/administradores/OrdenesPago")

@empleados.route("/administradores/OrdenEspecifica/statusEntregado/<string:id>")
def statusEntregado(id):
    with mysql.connection.cursor() as cursor:
        cursor.execute("UPDATE ordenpago SET status = 'Entregado' WHERE Id_Orden = %s", (id,))
        mysql.connection.commit()
    return redirect("/administradores/OrdenesPago")

@empleados.route("/administradores/OrdenEspecifica/crearorden/<string:id>")
def crearorden(id):

    with mysql.connection.cursor() as cursor:
        cursor.execute("INSERT INTO ordenpago(Id_Orden, Id_Usuario, Fecha, Status) VALUES (NULL, %s, NOW(), 'Pagado, recoger en caja')", (id,))
        mysql.connection.commit()
    return redirect("/administradores/OrdenesPago")

@empleados.route("/administradores/OrdenEspecifica/<string:id>")
def OrdenUsuario(id):
    with mysql.connect.cursor() as cursor:
        
        cursor.execute("SELECT Carrito FROM Usuarios WHERE Id_Usuario = %s",id,)
        fetch = cursor.fetchone()
        print(fetch)
        if not fetch or not fetch[0]:
            numero = 0
            productos = []
        else:
            
            carrito = fetch[0].split('|')[1:] # se elimina el primer elemento vacío de la lista
            
            numero = len(carrito)
            productos = []
            i = 0
            for producto in carrito:
                producto = producto.split(',')
                productos.append(producto)

                cursor.execute("SELECT Color_RGBA FROM productos WHERE Id_Productos = %s",producto[0],)
                color = cursor.fetchone()[0].split(',')

                producto[2] = int(producto[2])
                indice_color = int(producto[2])-1

                productos[i].append(color[indice_color])


                cursor.execute("SELECT Nombre,Precio FROM productos WHERE Id_Productos = %s",productos[i][0],)
                datos = cursor.fetchone()
                
                productos[i].extend(datos)
                
                i+=1
             
        cursor.execute("SELECT Nombre FROM Usuarios WHERE Id_Usuario = %s",id,)    
        nombre = cursor.fetchone()[0]

        cursor.execute("SELECT Id_Orden, Fecha FROM ordenpago WHERE Id_Usuario = %s",id,)
        orden = cursor.fetchone()
        print(orden)
    return render_template("empleados/OrdenEspecifica.jinja",id=id,numero = numero,productos=productos, nombre=nombre, orden = orden)

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
        with mysql.connect.cursor() as cursor:
            cursor.execute("SELECT MAX(Id_cuenta) FROM cuenta")
            max_id = cursor.fetchone() # esta linea es para obtener el primer valor y verifique que no se encuentre vacia
            id_nuevo = max_id[0]+1
            #Insertar en la tabla cuenta con el id máximo + 1
        with mysql.connection.cursor() as cursor:
            print(id_nuevo)
            cursor.execute("INSERT INTO cuenta(Id_cuenta, Rol, Correo, Contraseña, estado) VALUES (%s, %s, %s, %s, %s)", (id_nuevo, tipo, email, password, 'Inactivo'))
            mysql.connection.commit()
            # Insertar en la tabla empleado con el mismo id_cuenta
            cursor.execute("INSERT INTO empleado(Id_Empleado, RFC, Nombre_Empleado, Telefono, Direccion, Tipo_Empleado) VALUES (%s, %s, %s, %s, %s, %s)", (id_nuevo, rfc, nombre, tel, direccion, tipo))
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