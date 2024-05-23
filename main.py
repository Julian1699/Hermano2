from flask import Flask, render_template, request, redirect, flash, url_for
import psycopg2
from psycopg2 import sql
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecrectkey'

# Conexión a la base de datos
def obtener_conexion():
    try:
        conn = psycopg2.connect(os.getenv('DATABASE_URL', 'postgresql://postgres:123456@db-postgres:5432/tryapi'))
        return conn
    except psycopg2.DatabaseError as e:
        print(f"Error al conectar a la base de datos: {e}")
        raise

# Ruta para la página de inicio
@app.route('/')
def inicio():
    return render_template('inicio.html')

# Ruta para el menú principal
@app.route('/menu')
def menu():
    return render_template('menu.html')

# Ruta para la página de cómo funciona
@app.route('/como_funciona')
def como_funciona():
    return render_template('como_funciona.html')

# Ruta para la página de contactanos
@app.route('/contactanos')
def contactanos():
    return render_template('contactanos.html')

# Ruta para la página de información general
@app.route('/informacion')
def informacion():
    return render_template('informacion.html')

# Ruta para mostrar todos los productos
@app.route('/productos')
def mostrar_productos():
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM Productos")
        productos = cursor.fetchall()
        
        # Calcular el valor total del stock
        cursor.execute("SELECT SUM(precio * stock_inicial) FROM Productos")
        valor_total_stock = cursor.fetchone()[0] or 0
        
        return render_template('productos.html', productos=productos, valor_total_stock=valor_total_stock)
    except psycopg2.Error as error:
        print("Error al cargar los datos:", error)
        flash("Error al cargar los datos")
        return render_template('productos.html', productos=[], valor_total_stock=0)
    finally:
        cursor.close()
        conexion.close()


# Ruta para mostrar el formulario de creación de producto
@app.route('/crear_producto', methods=['GET'])
def mostrar_formulario_creacion():
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT id, nombre FROM Categorias")
        categorias = cursor.fetchall()
        
        cursor.execute("SELECT id, nombre FROM Proveedores")
        proveedores = cursor.fetchall()
        
        cursor.execute("SELECT id, nombre FROM Bodegas")
        bodegas = cursor.fetchall()
        
        return render_template('crear_producto.html', categorias=categorias, proveedores=proveedores, bodegas=bodegas)
    except psycopg2.Error as error:
        print("Error al cargar los datos:", error)
        flash("Error al cargar los datos")
        return render_template('crear_producto.html', categorias=[], proveedores=[], bodegas=[])
    finally:
        cursor.close()
        conexion.close()


# Ruta para procesar el formulario de creación de producto
@app.route('/crear_producto', methods=['POST'])
def crear_producto():
    conexion = obtener_conexion()
    try:
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        stock_inicial = request.form['stock_inicial']
        categoria_id = request.form['categoria_id']
        proveedor_id = request.form['proveedor_id']
        bodega_id = request.form['bodega_id']

        cursor = conexion.cursor()
        cursor.execute("INSERT INTO Productos (nombre, descripcion, precio, stock_inicial, categoria_id, proveedor_id, bodega_id) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                       (nombre, descripcion, precio, stock_inicial, categoria_id, proveedor_id, bodega_id))
        conexion.commit()

        flash('Producto creado correctamente')
        return redirect(url_for('mostrar_productos'))
    except psycopg2.Error as error:
        print("Error al crear el producto:", error)
        flash("Error al crear el producto")
        return redirect(url_for('mostrar_formulario_creacion'))
    finally:
        cursor.close()
        conexion.close()

# Ruta para mostrar el formulario de actualización de producto
@app.route('/actualizar_producto/<int:id>', methods=['GET'])
def mostrar_formulario_actualizacion(id):
    conexion = obtener_conexion()
    cursor = None
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM Productos WHERE id = %s", (id,))
        producto = cursor.fetchone()
        
        cursor.execute("SELECT id, nombre FROM Categorias")
        categorias = cursor.fetchall()
        
        cursor.execute("SELECT id, nombre FROM Proveedores")
        proveedores = cursor.fetchall()
        
        cursor.execute("SELECT id, nombre FROM Bodegas")
        bodegas = cursor.fetchall()
        
        return render_template('actualizar_producto.html', producto=producto, categorias=categorias, proveedores=proveedores, bodegas=bodegas)
    except psycopg2.Error as error:
        print("Error al cargar el producto:", error)
        flash("Error al cargar el producto")
        return redirect(url_for('mostrar_productos'))
    finally:
        if cursor:
            cursor.close()
        conexion.close()


# Ruta para procesar el formulario de actualización de producto
@app.route('/actualizar_producto/<int:id>', methods=['POST'])
def actualizar_producto(id):
    conexion = obtener_conexion()
    cursor = None
    try:
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        stock_inicial = request.form['stock_inicial']
        categoria_id = request.form['categoria_id']
        proveedor_id = request.form['proveedor_id']
        bodega_id = request.form['bodega_id']

        cursor = conexion.cursor()
        cursor.execute("UPDATE Productos SET nombre = %s, descripcion = %s, precio = %s, stock_inicial = %s, categoria_id = %s, proveedor_id = %s, bodega_id = %s WHERE id = %s",
                       (nombre, descripcion, precio, stock_inicial, categoria_id, proveedor_id, bodega_id, id))
        conexion.commit()

        flash('Producto actualizado correctamente')
        return redirect(url_for('mostrar_productos'))
    except psycopg2.Error as error:
        print("Error al actualizar el producto:", error)
        flash("Error al actualizar el producto")
        return redirect(url_for('mostrar_formulario_actualizacion', id=id))
    except KeyError as e:
        print(f"KeyError: {e}")
        flash(f"Faltan campos requeridos: {e}")
        return redirect(url_for('mostrar_formulario_actualizacion', id=id))
    finally:
        if cursor:
            cursor.close()
        conexion.close()

# Ruta para eliminar un producto
@app.route('/borrar_producto/<int:id>', methods=['POST'])
def borrar_producto(id):
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM Productos WHERE id = %s", (id,))
        conexion.commit()

        flash('Producto borrado correctamente')
        return redirect(url_for('mostrar_productos'))
    except psycopg2.Error as error:
        print("Error al borrar el producto:", error)
        flash("Error al borrar el producto")
        return redirect(url_for('mostrar_productos'))
    finally:
        cursor.close()
        conexion.close()

# Rutas para gestionar proveedores
@app.route('/proveedores')
def mostrar_proveedores():
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM Proveedores")
        proveedores = cursor.fetchall()
        return render_template('proveedores.html', proveedores=proveedores)
    except psycopg2.Error as error:
        print("Error al cargar los datos:", error)
        flash("Error al cargar los datos")
        return render_template('proveedores.html', proveedores=[])
    finally:
        cursor.close()
        conexion.close()

@app.route('/crear_proveedor', methods=['GET'])
def mostrar_formulario_creacion_proveedor():
    return render_template('crear_proveedor.html')

@app.route('/crear_proveedor', methods=['POST'])
def crear_proveedor():
    conexion = obtener_conexion()
    try:
        nombre = request.form['nombre']
        direccion = request.form['direccion']
        telefono = request.form['telefono']

        cursor = conexion.cursor()
        cursor.execute("INSERT INTO Proveedores (nombre, direccion, telefono) VALUES (%s, %s, %s)",
                       (nombre, direccion, telefono))
        conexion.commit()

        flash('Proveedor creado correctamente')
        return redirect(url_for('mostrar_proveedores'))
    except psycopg2.Error as error:
        print("Error al crear el proveedor:", error)
        flash("Error al crear el proveedor")
        return redirect(url_for('mostrar_formulario_creacion_proveedor'))
    finally:
        cursor.close()
        conexion.close()

@app.route('/actualizar_proveedor/<int:id>', methods=['GET'])
def mostrar_formulario_actualizacion_proveedor(id):
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM Proveedores WHERE id = %s", (id,))
        proveedor = cursor.fetchone()
        return render_template('actualizar_proveedor.html', proveedor=proveedor)
    except psycopg2.Error as error:
        print("Error al cargar el proveedor:", error)
        flash("Error al cargar el proveedor")
        return redirect(url_for('mostrar_proveedores'))
    finally:
        cursor.close()
        conexion.close()

@app.route('/actualizar_proveedor/<int:id>', methods=['POST'])
def actualizar_proveedor(id):
    conexion = obtener_conexion()
    try:
        nombre = request.form['nombre']
        direccion = request.form['direccion']
        telefono = request.form['telefono']

        cursor = conexion.cursor()
        cursor.execute("UPDATE Proveedores SET nombre = %s, direccion = %s, telefono = %s WHERE id = %s",
                       (nombre, direccion, telefono, id))
        conexion.commit()

        flash('Proveedor actualizado correctamente')
        return redirect(url_for('mostrar_proveedores'))
    except psycopg2.Error as error:
        print("Error al actualizar el proveedor:", error)
        flash("Error al actualizar el proveedor")
        return redirect(url_for('mostrar_formulario_actualizacion_proveedor', id=id))
    finally:
        cursor.close()
        conexion.close()

@app.route('/borrar_proveedor/<int:id>', methods=['POST'])
def borrar_proveedor(id):
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM Proveedores WHERE id = %s", (id,))
        conexion.commit()

        flash('Proveedor borrado correctamente')
        return redirect(url_for('mostrar_proveedores'))
    except psycopg2.Error as error:
        print("Error al borrar el proveedor:", error)
        flash("Error al borrar el proveedor")
        return redirect(url_for('mostrar_proveedores'))
    finally:
        cursor.close()
        conexion.close()

# Rutas para gestionar bodegas
@app.route('/bodegas')
def mostrar_bodegas():
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM Bodegas")
        bodegas = cursor.fetchall()
        return render_template('bodegas.html', bodegas=bodegas)
    except psycopg2.Error as error:
        print("Error al cargar los datos:", error)
        flash("Error al cargar los datos")
        return render_template('bodegas.html', bodegas=[])
    finally:
        cursor.close()
        conexion.close()

@app.route('/crear_bodega', methods=['GET'])
def mostrar_formulario_creacion_bodega():
    return render_template('crear_bodega.html')

@app.route('/crear_bodega', methods=['POST'])
def crear_bodega():
    conexion = obtener_conexion()
    try:
        nombre = request.form['nombre']
        ubicacion = request.form['ubicacion']
        capacidad_maxima = request.form['capacidad_maxima']

        cursor = conexion.cursor()
        cursor.execute("INSERT INTO Bodegas (nombre, ubicacion, capacidad_maxima) VALUES (%s, %s, %s)",
                       (nombre, ubicacion, capacidad_maxima))
        conexion.commit()

        flash('Bodega creada correctamente')
        return redirect(url_for('mostrar_bodegas'))
    except psycopg2.Error as error:
        print("Error al crear la bodega:", error)
        flash("Error al crear la bodega")
        return redirect(url_for('mostrar_formulario_creacion_bodega'))
    finally:
        cursor.close()
        conexion.close()

@app.route('/actualizar_bodega/<int:id>', methods=['GET'])
def mostrar_formulario_actualizacion_bodega(id):
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM Bodegas WHERE id = %s", (id,))
        bodega = cursor.fetchone()
        return render_template('actualizar_bodega.html', bodega=bodega)
    except psycopg2.Error as error:
        print("Error al cargar la bodega:", error)
        flash("Error al cargar la bodega")
        return redirect(url_for('mostrar_bodegas'))
    finally:
        cursor.close()
        conexion.close()

@app.route('/actualizar_bodega/<int:id>', methods=['POST'])
def actualizar_bodega(id):
    conexion = obtener_conexion()
    try:
        nombre = request.form['nombre']
        ubicacion = request.form['ubicacion']
        capacidad_maxima = request.form['capacidad_maxima']

        cursor = conexion.cursor()
        cursor.execute("UPDATE Bodegas SET nombre = %s, ubicacion = %s, capacidad_maxima = %s WHERE id = %s",
                       (nombre, ubicacion, capacidad_maxima, id))
        conexion.commit()

        flash('Bodega actualizada correctamente')
        return redirect(url_for('mostrar_bodegas'))
    except psycopg2.Error as error:
        print("Error al actualizar la bodega:", error)
        flash("Error al actualizar la bodega")
        return redirect(url_for('mostrar_formulario_actualizacion_bodega', id=id))
    finally:
        cursor.close()
        conexion.close()

@app.route('/borrar_bodega/<int:id>', methods=['POST'])
def borrar_bodega(id):
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM Bodegas WHERE id = %s", (id,))
        conexion.commit()

        flash('Bodega borrada correctamente')
        return redirect(url_for('mostrar_bodegas'))
    except psycopg2.Error as error:
        print("Error al borrar la bodega:", error)
        flash("Error al borrar la bodega")
        return redirect(url_for('mostrar_bodegas'))
    finally:
        cursor.close()
        conexion.close()

# Rutas para gestionar categorías
@app.route('/categorias')
def mostrar_categorias():
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM Categorias")
        categorias = cursor.fetchall()
        return render_template('categorias.html', categorias=categorias)
    except psycopg2.Error as error:
        print("Error al cargar los datos:", error)
        flash("Error al cargar los datos")
        return render_template('categorias.html', categorias=[])
    finally:
        cursor.close()
        conexion.close()

@app.route('/crear_categoria', methods=['GET'])
def mostrar_formulario_creacion_categoria():
    return render_template('crear_categoria.html')

@app.route('/crear_categoria', methods=['POST'])
def crear_categoria():
    conexion = obtener_conexion()
    try:
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']

        cursor = conexion.cursor()
        cursor.execute("INSERT INTO Categorias (nombre, descripcion) VALUES (%s, %s)",
                       (nombre, descripcion))
        conexion.commit()

        flash('Categoría creada correctamente')
        return redirect(url_for('mostrar_categorias'))
    except psycopg2.Error as error:
        print("Error al crear la categoría:", error)
        flash("Error al crear la categoría")
        return redirect(url_for('mostrar_formulario_creacion_categoria'))
    finally:
        cursor.close()
        conexion.close()

@app.route('/actualizar_categoria/<int:id>', methods=['GET'])
def mostrar_formulario_actualizacion_categoria(id):
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM Categorias WHERE id = %s", (id,))
        categoria = cursor.fetchone()
        return render_template('actualizar_categoria.html', categoria=categoria)
    except psycopg2.Error as error:
        print("Error al cargar la categoría:", error)
        flash("Error al cargar la categoría")
        return redirect(url_for('mostrar_categorias'))
    finally:
        cursor.close()
        conexion.close()

@app.route('/actualizar_categoria/<int:id>', methods=['POST'])
def actualizar_categoria(id):
    conexion = obtener_conexion()
    try:
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']

        cursor = conexion.cursor()
        cursor.execute("UPDATE Categorias SET nombre = %s, descripcion = %s WHERE id = %s",
                       (nombre, descripcion, id))
        conexion.commit()

        flash('Categoría actualizada correctamente')
        return redirect(url_for('mostrar_categorias'))
    except psycopg2.Error as error:
        print("Error al actualizar la categoría:", error)
        flash("Error al actualizar la categoría")
        return redirect(url_for('mostrar_formulario_actualizacion_categoria', id=id))
    finally:
        cursor.close()
        conexion.close()

@app.route('/borrar_categoria/<int:id>', methods=['POST'])
def borrar_categoria(id):
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM Categorias WHERE id = %s", (id,))
        conexion.commit()

        flash('Categoría borrada correctamente')
        return redirect(url_for('mostrar_categorias'))
    except psycopg2.Error as error:
        print("Error al borrar la categoría:", error)
        flash("Error al borrar la categoría")
        return redirect(url_for('mostrar_categorias'))
    finally:
        cursor.close()
        conexion.close()

## Mostrar Informes Finales de Proveedores, Bodegas y Categorias

@app.route('/categoria/<int:id>', methods=['GET'])
def consultar_categoria(id):
    conexion = obtener_conexion()
    cursor = None
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT nombre, descripcion FROM Categorias WHERE id = %s", (id,))
        categoria = cursor.fetchone()
        
        cursor.execute("SELECT id, nombre, descripcion FROM Productos WHERE categoria_id = %s", (id,))
        productos = cursor.fetchall()
        
        return render_template('categoria_detalle.html', categoria=categoria, productos=productos)
    except psycopg2.Error as error:
        print("Error al cargar la categoría:", error)
        flash("Error al cargar la categoría")
        return redirect(url_for('mostrar_categorias'))
    finally:
        if cursor:
            cursor.close()
        conexion.close()


@app.route('/proveedor/<int:id>', methods=['GET'])
def consultar_proveedor(id):
    conexion = obtener_conexion()
    cursor = None
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT nombre, direccion, telefono FROM Proveedores WHERE id = %s", (id,))
        proveedor = cursor.fetchone()
        
        cursor.execute("SELECT id, nombre, descripcion FROM Productos WHERE proveedor_id = %s", (id,))
        productos = cursor.fetchall()
        
        return render_template('proveedor_detalle.html', proveedor=proveedor, productos=productos)
    except psycopg2.Error as error:
        print("Error al cargar el proveedor:", error)
        flash("Error al cargar el proveedor")
        return redirect(url_for('mostrar_proveedores'))
    finally:
        if cursor:
            cursor.close()
        conexion.close()

@app.route('/bodega/<int:id>', methods=['GET'])
def consultar_bodega(id):
    conexion = obtener_conexion()
    cursor = None
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT nombre, ubicacion, capacidad_maxima FROM Bodegas WHERE id = %s", (id,))
        bodega = cursor.fetchone()
        
        cursor.execute("SELECT id, nombre, descripcion FROM Productos WHERE bodega_id = %s", (id,))
        productos = cursor.fetchall()
        
        return render_template('bodega_detalle.html', bodega=bodega, productos=productos)
    except psycopg2.Error as error:
        print("Error al cargar la bodega:", error)
        flash("Error al cargar la bodega")
        return redirect(url_for('mostrar_bodegas'))
    finally:
        if cursor:
            cursor.close()
        conexion.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0')
