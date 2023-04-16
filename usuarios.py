import flask
import requests
from flask import session, render_template, redirect, jsonify, make_response, url_for, request
from flask_mysqldb import MySQL
from collections import OrderedDict

usuarios = flask.Blueprint('usuarios', __name__)
mysql = MySQL()

@usuarios.record_once
def on_load(state):
    app = state.app
    mysql.init_app(app)

@usuarios.route("/productsApi")
@usuarios.route("/productsApi/<id>", methods=['GET'])
def productsApi(id=0):
    keys = [
    'Id',
    'Nombre', 
    'Imagenes',
    'Descripcion',
    'Precio u.',
    'Nombre color',
    'Hex color',
    'Categoria',
    'Recomendacion',
    'Marca',
    'Stock',
    'Tipo de piel',
    'Imagenes filtro',
    'Tipo'
    ]
    
    arr = []
    colors = {}


    with mysql.connect.cursor() as cursor:
        if id != 0:
            cursor.execute("SELECT * FROM productos WHERE Id_Productos = %s", (id,))
            rows = cursor.fetchone()
            ord = OrderedDict(zip(keys, rows))
            # Dividir los nombres de colores y los valores de Hex
            color_names = ord['Nombre color'].split(',')
            hex_values = ord['Hex color'].split(',')

            # Crear un nuevo JSON para cada color
            colors = {}
            for i, name in enumerate(color_names):
                colors[i+1] = {'Nombre': name, 'Hex': hex_values[i]}

            # Reemplazar 'Nombre color' y 'Hex color' con el nuevo JSON
            ord['Colores'] = colors
            del ord['Nombre color']
            del ord['Hex color']
            arr.append(ord)
        else:
            cursor.execute("SELECT * FROM productos")
            rows = cursor.fetchall()
            for item in rows:
                ord = OrderedDict(zip(keys, item))
                # Dividir los nombres de colores y los valores de Hex
                color_names = ord['Nombre color'].split(',')
                hex_values = ord['Hex color'].split(',')

                # Crear un nuevo JSON para cada color
                colors = {}
                for i, name in enumerate(color_names):
                    colors[i+1] = {'Nombre': name, 'Hex': hex_values[i]}

                # Reemplazar 'Nombre color' y 'Hex color' con el nuevo JSON
                ord['Colores'] = colors
                del ord['Nombre color']
                del ord['Hex color']

                arr.append(ord)

    response = make_response(jsonify({
            'Productos': arr
        }), 200)

    response.headers["Content-type"] = "application/json"
    return response

@usuarios.route("/usuarios")
def index():
    link = url_for('usuarios.productsApi', _external=True)
    response = requests.get(link).json()
    data = response['Productos']

    with mysql.connect.cursor() as cursor:
        cursor.execute("SELECT Carrito FROM Usuarios WHERE Id_Usuario = %s", (session.get('id_usuario'),))
        fetch = cursor.fetchone()
        if fetch is None or not fetch[0]:
            numero = 0
        else:
            abubu = fetch[0].split("|")
            numero = len(abubu)
    return render_template("usuarios/landing.jinja", productos = data, idUsuario = session.get('id_usuario'), carrito = numero)

@usuarios.route("/usuarios/addcarrito", methods=['POST'])
def addcarrito():
    carritoData = request.form['carritoData']
    idUsuario = request.form['id']
    print(carritoData)
    print(idUsuario)
    with mysql.connection.cursor() as cursor:
        cursor.execute("UPDATE usuarios SET Carrito = CONCAT(Carrito, %s) WHERE id_Usuario = %s", (carritoData, idUsuario))
        mysql.connection.commit()
        cursor.close()
    return redirect("/")

@usuarios.route('/usuarios/eliminar_producto/<string:id>', methods=['POST'])
def eliminar_producto(id):
    ids = id.split('_')
    id_producto = int(ids[0])-1
    id = ids[1]
    print(id)
    print(id_producto)
    with mysql.connect.cursor() as cursor:
        cursor.execute("SELECT Carrito FROM Usuarios WHERE Id_Usuario = %s",id,)
        fetch = cursor.fetchone()
        carrito = fetch[0].split('|')[1:] # se elimina el primer elemento vacío de la lista
        print(carrito)
        del carrito[id_producto]
        print(carrito)
        carrito_str = '|'.join(carrito)
        carrito_str = "|"+carrito_str
        print(carrito_str)
    with mysql.connection.cursor() as cursor:
        cursor.execute("UPDATE usuarios SET Carrito = %s WHERE id_Usuario = %s", (carrito_str, id))
        mysql.connection.commit()
        cursor.close()
    return 'OK'

@usuarios.route("/usuarios/ordencarrito/<string:id>", methods=['POST','GET'])
def ordencarrito(id):
    print(id)
    with mysql.connect.cursor() as cursor:
        
        cursor.execute("SELECT Carrito FROM Usuarios WHERE Id_Usuario = %s",id,)
        fetch = cursor.fetchone()
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

                #print(color[int(productos[int(productos[i][2])])])
                cursor.execute("SELECT Nombre,Precio FROM productos WHERE Id_Productos = %s",productos[i][0],)
                datos = cursor.fetchone()
                
                productos[i].extend(datos)
                
                i+=1
        cursor.execute("SELECT Nombre FROM Usuarios WHERE Id_Usuario = %s",id,)    
        nombre = cursor.fetchone()[0]
        
    return render_template("usuarios/CarritoCompras.jinja",id=id,numero = numero,productos=productos, nombre=nombre)


@usuarios.route("/cam")
def cam():
    return render_template("usuarios/cam.jinja")