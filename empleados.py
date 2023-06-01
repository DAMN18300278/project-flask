from flask_mysqldb import MySQL
from flask import render_template, session, redirect, flash, Blueprint, request, url_for
import os
import schedule
import time
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
import requests
from datetime import datetime, timedelta


empleados = Blueprint('empleados', __name__)
mysql = MySQL()
mail = Mail()
@empleados.record_once
def on_load(state):
    app = state.app
    mysql.init_app(app)
    mail.init_app(app)

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
        nombre = request.form['Nombre']
        imagenes = request.files.getlist('Imagen[]')
        num_imagenes = len(imagenes)

        index = 1
        ruta_completa = os.path.join(os.getcwd(), 'static', 'src')
        with mysql.connect.cursor() as cursor:
            cursor.execute("SELECT MAX(Id_Productos) from productos")
            id_producto = cursor.fetchone()[0] + 1

        for imagen in imagenes:
            imagen.filename = "img" + str(id_producto) + "_" + str(index) + ".jpg"
            filename = secure_filename(imagen.filename)
            with open(os.path.join(ruta_completa, filename), 'wb') as f:
                f.write(imagen.read())
            index+= 1

        descripcion = request.form['Descripcion']
        precio = request.form['Precio']
        
        nombre_color = request.form.getlist('nombre_color') # Obtener la lista de nombres de colores
        color_rgba = request.form.getlist('color') # Obtener la lista de valores hexadecimales de colores
        # Convertir las listas en strings separados por comas
        for i in range(len(color_rgba)):
            color_rgba[i] = color_rgba[i].replace('#', '')
        nombre_color = ','.join(nombre_color)
        color_rgba = ','.join(color_rgba)
       
        categoria = request.form['Categoria']
        cantidad = request.form['Cantidad']
        marca = request.form['Marca']
        tipo_piel = request.form['TipoPiel']
        tipo = request.form['Tipo']
        recomendacion = request.form['Recomendacion']
        imagen_filtro = request.files.getlist('Imagen_fil[]')
        filtronames = ','.join([file.filename for file in imagen_filtro])

    with mysql.connection.cursor() as cursor:
            cursor.execute("INSERT INTO productos(Nombre, Imagen, Descripcion, Precio, Nombre_Color, Color_RGBA, Categoria, Recomendacion, Marca, Cantidad , Tipo_Piel, Imagen_filtro, Tipo) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", ( nombre,num_imagenes, descripcion, precio, nombre_color, color_rgba, categoria, recomendacion, marca, cantidad, tipo_piel, filtronames, tipo))
            mysql.connection.commit()
            
    return redirect("/administradores/inventario")

@empleados.route("/administradores/editarProducto/UpdateProducto/<int:id>", methods=['POST','GET'])
def modificar_producto(id):
    if request.method == 'POST':
        nombre = request.form['Nombre']
        imagenes = request.files.getlist('Imagen[]')
        num_imagenes = 0

        if imagenes[0].filename != "":
            num_imagenes = len(imagenes)
            index = 1
            ruta_completa = os.path.join(os.getcwd(), 'static', 'src')
            archivos = os.listdir(ruta_completa)

            for archivo in archivos:
                if archivo.startswith('img' + str(id) + '_'):
                    ruta_archivo = os.path.join(ruta_completa, archivo)
                    os.remove(ruta_archivo)

            for imagen in imagenes:
                imagen.filename = "img" + str(id) + "_" + str(index) + ".jpg"
                filename = secure_filename(imagen.filename)
                with open(os.path.join(ruta_completa, filename), 'wb') as f:
                    f.write(imagen.read())
                index+= 1


        descripcion = request.form['Descripcion']
        precio = request.form['Precio']
        
        nombre_color = request.form.getlist('nombre_color') # Obtener la lista de nombres de colores
        color_rgba = request.form.getlist('color') # Obtener la lista de valores hexadecimales de colores
        # Convertir las listas en strings separados por comas
        for i in range(len(color_rgba)):
            color_rgba[i] = color_rgba[i].replace('#', '')
        nombre_color = ','.join(nombre_color)
        color_rgba = ','.join(color_rgba)
       
        categoria = request.form['Categoria']
        cantidad = request.form['Cantidad']
        marca = request.form['Marca']
        tipo_piel = request.form['TipoPiel']
        tipo = request.form['Tipo']
        recomendacion = request.form['Recomendacion']
        imagen_filtro = request.files.getlist('Imagen_fil[]')
        filtronames = ','.join([file.filename for file in imagen_filtro])

    with mysql.connection.cursor() as cursor:
            if num_imagenes > 0:
                cursor.execute("UPDATE productos SET Nombre = %s, Imagen = %s, Descripcion = %s, Precio = %s, Nombre_Color = %s, Color_RGBA = %s, Categoria = %s, Recomendacion = %s, Marca = %s, Cantidad = %s, Tipo_Piel = %s, Imagen_filtro = %s, Tipo = %s WHERE Id_Productos = %s", ( nombre,num_imagenes, descripcion, precio, nombre_color, color_rgba, categoria, recomendacion, marca, cantidad, tipo_piel, filtronames, tipo, id))
            else:
                cursor.execute("UPDATE productos SET Nombre = %s, Descripcion = %s, Precio = %s, Nombre_Color = %s, Color_RGBA = %s, Categoria = %s, Recomendacion = %s, Marca = %s, Cantidad = %s, Tipo_Piel = %s, Imagen_filtro = %s, Tipo = %s WHERE Id_Productos = %s", ( nombre, descripcion, precio, nombre_color, color_rgba, categoria, recomendacion, marca, cantidad, tipo_piel, filtronames, tipo, id))

            mysql.connection.commit()
            
    return redirect("/administradores/inventario")



@empleados.route("/administradores/EmpleadosList")
def EmpAdmin():
    _, tipo = asignarNombre()
    with mysql.connect.cursor() as cursor:
        cursor.execute("SELECT empleado.Id_Empleado, empleado.Nombre_Empleado, rol.Rol FROM empleado INNER JOIN cuenta ON empleado.Id_Empleado = cuenta.Id_cuenta INNER JOIN rol ON cuenta.Rol = rol.Id_Rol WHERE empleado.Id_Empleado != 0 ORDER BY empleado.Id_Empleado ASC")
        resultado = cursor.fetchall()
    return render_template("empleados/EmpleadosList.jinja", resultados = resultado, tipo = tipo)

@empleados.route('/administradores/editarEmpleados', methods=['POST', 'GET'])
@empleados.route('/administradores/editarEmpleados/<int:id>', methods=['POST', 'GET'])
def Admin_empleados_Edit(id=None):
    _, tipo = asignarNombre()
    if id:
        with mysql.connect.cursor() as cursor:
            cursor.execute("SELECT empleado.Nombre_Empleado, cuenta.Correo, cuenta.Contraseña, empleado.RFC, empleado.Direccion, empleado.Telefono, rol.rol, empleado.Id_Empleado FROM empleado INNER JOIN cuenta ON empleado.Id_Empleado = cuenta.Id_cuenta INNER JOIN rol ON cuenta.Rol = rol.Id_Rol WHERE empleado.Id_Empleado = %s", (id,))
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
    _, tipo = asignarNombre()
    with mysql.connect.cursor() as cursor:
        cursor.execute("SELECT OrdenPago.Id_Orden, usuarios.Nombre ,OrdenPago.Fecha, OrdenPago.Status, OrdenPago.Id_Usuario FROM OrdenPago INNER JOIN usuarios ON usuarios.Id_Usuario = OrdenPago.Id_Usuario ORDER BY Id_Orden ASC")
        resultado = cursor.fetchall()
    return render_template("empleados/OrdenesPago.jinja", resultados = resultado,tipo = tipo)



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
        cursor.execute("SELECT Correo FROM usuarios WHERE Id_Usuario = %s", (id,))
        print(result)
        if result and result[0] == 'activo':  # Verificar si existe el registro y si el estatus es 'activo'
            
            flash('pedido activo.')
            return redirect("/usuarios/ordencarrito/"+id)
        else:
            with mysql.connect.cursor() as cursor:
                cursor.execute("SELECT carrito From usuarios where Id_Usuario = %s",(id,))
                fetch = cursor.fetchone()
                carrito = fetch[0].split('|') 
                
                numero = len(carrito)
                
                i = 0
                for producto in carrito:
                    producto = producto.split(',')
                    productos.append(producto)
                 
                    with mysql.connect.cursor() as cursor:
                        cursor.execute("SELECT Cantidad,Nombre From productos where Id_Productos = %s",(producto[0],))
                        result = cursor.fetchone()
                        cantidad = int(result[0])
                        nombre= result[1]
                       
                        if cantidad > int(producto[1]) :
                            cantidad = cantidad - int(producto[1])

                            with mysql.connection.cursor() as cursor:
                                cursor.execute("UPDATE productos SET Cantidad = %s WHERE Id_Productos = %s", (cantidad,producto[0]))
                        else:
                                flash('No hay suficiente cantidad del producto ' + nombre)
                                return redirect("/usuarios/ordencarrito/"+id)
            with mysql.connection.cursor() as cursor:
                cursor.execute("INSERT INTO ordenpago(Id_Orden, Id_Usuario, Fecha, Status) VALUES (NULL, %s, NOW(), 'Pagado, recoger en caja')", (id,))
                cursor.execute("UPDATE usuarios SET Estatus_Pedido = 'activo' WHERE Id_Usuario = %s", (id,))
                mysql.connection.commit()
            flash('Se ha insertado la orden de pago exitosamente.')
            numeroorden(id)
            actualizaredad(id)
    return redirect("/administradores/OrdenesPago")

@empleados.route("/administradores/OrdenEspecifica/<string:id>")
def OrdenUsuario(id):

    with mysql.connect.cursor() as cursor:
        
        cursor.execute("SELECT Carrito, Id_Usuario, Status FROM ordenpago WHERE Id_Orden = %s",(id,))
        fetch = cursor.fetchone()
        status = fetch[2]
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
    return render_template("empleados/OrdenEspecifica.jinja",id=id,status=status,numero = numero,productos=productos, nombre=nombre, orden = orden)

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
            cursor.execute("UPDATE cuenta SET Correo = %s, Contraseña = %s, Rol = %s WHERE Id_cuenta = %s", (email, password,tipo, id))
            mysql.connection.commit()
            cursor.execute("UPDATE empleado SET RFC = %s, Nombre_Empleado = %s, Telefono = %s, Direccion = %s WHERE Id_Empleado = %s",(rfc, nombre, tel, direccion, id))
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


@empleados.route("/administradores/reportedeescazes/<int:id>", methods=['POST'])
@empleados.route("/administradores/reportedeescazes", methods=['POST'])
def procesar_reporte(id=None):
    fecha = datetime.now().strftime('%d/%m/%Y')  # Obtiene la fecha actual

    with mysql.connect.cursor() as cursor:
        cursor.execute("SELECT Nombre, Cantidad FROM productos WHERE Id_Productos = %s", (id,))
        resultados = cursor.fetchone()

    if id:
        subject = "Reporte de Escasez"
        producto_nombre = resultados[0]
        producto_cantidad = resultados[1]
        reporte = f"Estimado Administrador,\n\nSe ha generado un reporte de escasez. El producto '{producto_nombre}' con ID {id} cuenta actualmente con {producto_cantidad} unidades en stock. Por favor, tome las medidas necesarias para abastecer el inventario.\n\nFecha del reporte: {fecha}\n\nSaludos,\nEquipo de Decore"
    else:
        reporte = request.form.get('reporteInput')
        subject = "Reporte"
        reporte = f"Estimado Administrador,\n\nSe ha generado un reporte. A continuación se muestra el contenido del reporte:\n\n{reporte}\n\nFecha del reporte: {fecha}\n\nSaludos,\nEquipo de Decore"

    with mysql.connect.cursor() as cursor:
        cursor.execute("SELECT Correo FROM cuenta WHERE Rol = 3 AND Id_cuenta <> 0")
        resultados = cursor.fetchall()

        for resultado in resultados:
            enviar_correo(resultado[0], subject, reporte)

    return redirect("/administradores/inventario")

def enviar_correo(destinatario, subject, reporte):
    sender = "decore.makeup.soporte@gmail.com"
    message = Message(subject, sender=sender, recipients=[destinatario])
    message.body = reporte
    mail.send(message)

@empleados.route('/administradores/BorrarOrden/<int:id>')
def borrarorden(id):
    with mysql.connect.cursor() as cursor:
        cursor.execute("SELECT * FROM ordenpago WHERE Id_Orden = %s", (id,))
        orden_pago = cursor.fetchone()

    if orden_pago and orden_pago[3] != "Entregado":
        carrito = orden_pago[4]
        productos = carrito.split('|')
        for producto_info in productos:
            producto = producto_info.split(',')
            producto_id = producto[0]
            cantidad = int(producto[1])

            # Actualizar el stock del producto
            with mysql.connection.cursor() as cursor:
                cursor.execute("UPDATE productos SET Cantidad = (Cantidad + %s) WHERE Id_Productos = %s", (cantidad, producto_id))

                mysql.connection.commit()

    with mysql.connection.cursor() as cursor:
        cursor.execute("DELETE FROM ordenpago WHERE Id_Orden = %s", (id,))
        cursor.execute("UPDATE usuarios SET Estatus_Pedido = 'inactivo' WHERE Id_Usuario = %s", (orden_pago[1],))
        mysql.connection.commit()

    return redirect("/administradores/OrdenesPago")


def numeroorden(id):
    subject = 'Pedido Realizado con éxito'
    sender = "decore.makeup.soporte@gmail.com"
    with mysql.connect.cursor() as cursor:
        cursor.execute("SELECT MAX(ordenpago.Id_Orden) AS Orden, cuenta.Correo FROM cuenta INNER JOIN usuarios ON cuenta.Id_Cuenta = usuarios.Id_Usuario INNER JOIN ordenpago ON usuarios.Id_Usuario = ordenpago.Id_Usuario WHERE cuenta.Id_Cuenta = 51 GROUP BY cuenta.Correo", (id,))
        resultado = cursor.fetchone()
    message = Message(subject, sender=sender, recipients=[resultado[1]])
    message.body = f"Estimado Cliente,\n\nSe ha realizado su pedido correctamente. Su número de orden es:\n\n{resultado[0]}\n\nSaludos,\nEquipo de Decore"
    mail.send(message)

def actualizaredad(id):
    with mysql.connect.cursor() as cursor:
        # Obtener la orden de pago con el Id_Orden más grande
        cursor.execute(" SELECT usuarios.Edad, ordenpago.carrito FROM usuarios INNER JOIN ordenpago ON ORDENPAGO.Id_Usuario = usuarios.Id_Usuario WHERE ordenpago.Id_Usuario = %s ORDER BY ordenpago.Id_Orden DESC LIMIT 1", (id,))
        result = cursor.fetchone()

        if result:
            carrito = result[1].split("|")  # Separar los valores por el carácter "|"
            edad = int(result[0])  # Obtener la edad del usuario
            
            with mysql.connection.cursor() as cursor:
                for item in carrito:
                    values = item.split(",")  # Separar los valores por el carácter ","
                    producto_id = int(values[0])  # Obtener el primer dígito (Id_Producto)
                    print(edad)
                    print(producto_id)
                    cursor.execute("UPDATE recomendacion SET Promedio_Edad = (Promedio_Edad + %s), NumVentas = (NumVentas+1) WHERE Id_Producto = %s", (edad, producto_id))
                mysql.connection.commit()

@empleados.route("/administradores/editarProducto/<int:id>", methods=['POST', 'GET'])
def editarProducto(id):
    link = url_for('usuarios.productsApi', _external=True, id = id)
    response = requests.get(link).json()
    data = response['Productos'][0]

    return render_template("empleados/InventarioNewProd.jinja", producto = data)
