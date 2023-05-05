from flask_mysqldb import MySQL
from flask import render_template, session, redirect, flash, Blueprint, request, url_for
import os
from werkzeug.utils import secure_filename

empleados = Blueprint('empleados', __name__)
mysql = MySQL()

@empleados.record_once
def on_load(state):
    app = state.app
    mysql.init_app(app)

def asignarNombre():
    with mysql.connect.cursor() as cursor:
        cursor.execute('SELECT empleado.Nombre_Empleado, cuenta.Rol FROM empleado INNER JOIN cuenta ON empleado.Id_Empleado = cuenta.Id_cuenta WHERE empleado.Id_Empleado = %s', (session.get('id_administrador'),))
        rows = cursor.fetchone()
        nombre = rows[0]
        tipo = rows[1]
        return nombre, tipo

@empleados.route("/administradores")
def indexAdmin():
    nombre, tipo = asignarNombre()
    return render_template("empleados/indexAdmin.jinja", nombre = nombre, tipo = tipo)

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
        imagenes = request.files.getlist('Imagen[]')
        num_imagenes = len(imagenes)

        index = 1
        os.chdir('/static/src')
        for imagen in imagenes:
            imagen.filename = "img" + str(id_producto) + "_" + str(index) + ".jpg"
            filename = secure_filename(imagen.filename)
            with open(imagen.name, 'wb') as f:
                f.write
                imagen.save(os.path.join('/static/src', filename))

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
    _, tipo = asignarNombre()
    with mysql.connect.cursor() as cursor:
        cursor.execute("SELECT empleado.Id_Empleado, empleado.Nombre_Empleado, rol.Rol FROM empleado INNER JOIN cuenta ON empleado.Id_Empleado = cuenta.Id_cuenta INNER JOIN rol ON cuenta.Rol = rol.Id_Rol ORDER BY empleado.Id_Empleado ASC")
        resultado = cursor.fetchall()
    return render_template("empleados/EmpleadosList.jinja", resultados = resultado, tipo = tipo)

@empleados.route('/administradores/editarEmpleados', methods=['POST', 'GET'])
@empleados.route('/administradores/editarEmpleados/<int:id>', methods=['POST', 'GET'])
def Admin_empleados_Edit(id=None):
    _, tipo = asignarNombre()
    if id:
        with mysql.connect.cursor() as cursor:
            cursor.execute("SELECT empleado.Nombre_Empleado, cuenta.Correo, cuenta.Contraseña ,empleado.RFC, empleado.Direccion, empleado.RFC, rol.rol, empleado.Id_Empleado FROM empleado INNER JOIN cuenta ON empleado.Id_Empleado = %s INNER JOIN rol ON cuenta.Rol = rol.Id_Rol", (id,))
            resultado = cursor.fetchone()
        return render_template("empleados/EmpEdit.jinja", empleado = resultado, tipo=tipo)
    else:
        return render_template("empleados/EmpEdit.jinja", empleado = "",tipo=tipo)

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
        cursor.execute("SELECT OrdenPago.Id_Orden, usuarios.Nombre ,OrdenPago.Fecha, OrdenPago.Status, OrdenPago.Id_Usuario FROM OrdenPago INNER JOIN usuarios ON usuarios.Id_Usuario = OrdenPago.Id_Usuario ORDER BY Id_Orden ASC")
        resultado = cursor.fetchall()
    return render_template("empleados/OrdenesPago.jinja", resultados = resultado)



@empleados.route("/administradores/OrdenEspecifica/statusEntregado/<string:id>")
def statusEntregado(id):
    with mysql.connect.cursor() as cursor:
        cursor.execute("SELECT Id_Usuario FROM ordenpago WHERE Id_Orden = %s",(id,))
        fetch = cursor.fetchone()
    with mysql.connection.cursor() as cursor:
        cursor.execute("UPDATE ordenpago SET status = 'Entregado' WHERE Id_Orden = %s", (id,))
        cursor.execute("UPDATE usuarios SET Estatus_Pedido = 'inactivo' WHERE Id_Usuario = %s", (fetch,))
        mysql.connection.commit()
        
    return redirect("/administradores/OrdenesPago")

@empleados.route("/administradores/OrdenEspecifica/crearorden/<string:id>")
def crearorden(id):

    with mysql.connect.cursor() as cursor:
        cursor.execute("SELECT Estatus_Pedido FROM usuarios WHERE Id_Usuario = %s", (id,))
        result = cursor.fetchone()
        print(result)
        if result and result[0] == 'activo':  # Verificar si existe el registro y si el estatus es 'activo'
            
            flash('pedido activo.')
            return redirect("/usuarios/ordencarrito/"+id)
        else:
            print(result)
            with mysql.connection.cursor() as cursor:
                cursor.execute("INSERT INTO ordenpago(Id_Orden, Id_Usuario, Fecha, Status) VALUES (NULL, %s, NOW(), 'Pagado, recoger en caja')", (id,))
                cursor.execute("UPDATE usuarios SET Estatus_Pedido = 'activo' WHERE Id_Usuario = %s", (id,))
                mysql.connection.commit()
            flash('Se ha insertado la orden de pago exitosamente.')
    return redirect("/administradores/OrdenesPago")

@empleados.route("/administradores/OrdenEspecifica/<string:id>")
def OrdenUsuario(id):

    with mysql.connect.cursor() as cursor:
        
        cursor.execute("SELECT Carrito, Id_Usuario FROM ordenpago WHERE Id_Orden = %s",(id,))
        fetch = cursor.fetchone()
        if not fetch or not fetch[0]:
            numero = 0
            productos = []
        else:
            
            carrito = fetch[0].split('|') # se elimina el primer elemento vacío de la lista
            
            numero = len(carrito)
            productos = []
            i = 0
            for producto in carrito:
                producto = producto.split(',')
                productos.append(producto)

                cursor.execute("SELECT Color_RGBA FROM productos WHERE Id_Productos = %s",(producto[0],))
                color = cursor.fetchone()[0].split(',')

                producto[2] = int(producto[2])
                indice_color = int(producto[2])-1

                productos[i].append(color[indice_color])

                cursor.execute("SELECT Nombre,Precio FROM productos WHERE Id_Productos = %s",(productos[i][0],))
                datos = cursor.fetchone()
                
                productos[i].extend(datos)
                
                i+=1
             
        cursor.execute("SELECT Nombre FROM Usuarios WHERE Id_Usuario = %s",(fetch[1],))    
        nombre = cursor.fetchone()[0]

        cursor.execute("SELECT Id_Orden, Fecha FROM ordenpago WHERE Id_Orden = %s",(id,))
        orden = cursor.fetchone()
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
            cursor.execute("UPDATE cuenta SET Correo = %s, Contraseña = %s, Rol = %s WHERE Id_cuenta = %s", (email, password, id))
            mysql.connection.commit()
            cursor.execute("UPDATE empleado SET RFC = %s, Nombre_Empleado = %s, Telefono = %s, Direccion = %s WHERE Id_Empleado = %s",(rfc, nombre, tel, direccion, tipo, id))
            mysql.connection.commit()
            
        return redirect("/administradores/EmpleadosList")
    else:
        with mysql.connect.cursor() as cursor:
            cursor.execute("SELECT MAX(Id_cuenta) FROM cuenta")
            max_id = cursor.fetchone() # esta linea es para obtener el primer valor y verifique que no se encuentre vacia
            id_nuevo = max_id[0]+1
            #Insertar en la tabla cuenta con el id máximo + 1
        with mysql.connection.cursor() as cursor:
            cursor.execute("INSERT INTO cuenta(Id_cuenta, Rol, Correo, Contraseña, estado) VALUES (%s, %s, %s, %s, %s)", (id_nuevo, tipo, email, password, 'Inactivo'))
            mysql.connection.commit()
            # Insertar en la tabla empleado con el mismo id_cuenta
            cursor.execute("INSERT INTO empleado(Id_Empleado, RFC, Nombre_Empleado, Telefono, Direccion) VALUES (%s, %s, %s, %s, %s)", (id_nuevo, rfc, nombre, tel, direccion))
            mysql.connection.commit()
            
        return redirect("/administradores/EmpleadosList") 


@empleados.route("/administradores/delete")
def delAdmin():
    session.clear()
    return redirect("/")
