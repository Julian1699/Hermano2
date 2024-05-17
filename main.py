from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
# Conexión a la base de datos
def obtener_conexion():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='123456789',
        database='hermano2'
    )

# Ruta para la página de inicio
@app.route('/')
def inicio():
    return render_template('inicio.html')

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
        cursor.execute("SELECT * FROM ProductosItienda")
        productos = cursor.fetchall()
        return render_template('productos.html', productos=productos)
    except mysql.connector.Error as error:
        print("Error al cargar los datos:", error)
        flash("Error al cargar los datos")
        return render_template('productos.html', productos=[])
    finally:
        cursor.close()
        conexion.close()

# Ruta para mostrar el formulario de creación de producto
@app.route('/crear_producto', methods=['GET'])
def mostrar_formulario_creacion():
    return render_template('crear_producto.html')

# Ruta para procesar el formulario de creación de producto
@app.route('/crear_producto', methods=['POST'])
def crear_producto():
    conexion = obtener_conexion()
    try:
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        stock_inicial = request.form['stock_inicial']

        cursor = conexion.cursor()
        cursor.execute("INSERT INTO ProductosItienda (nombre, descripcion, precio, stock_inicial) VALUES (%s, %s, %s, %s)",
                       (nombre, descripcion, precio, stock_inicial))
        conexion.commit()

        flash('Producto creado correctamente')
        return redirect(url_for('mostrar_productos'))
    except mysql.connector.Error as error:
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
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM ProductosItienda WHERE id = %s", (id,))
        producto = cursor.fetchone()
        return render_template('actualizar_producto.html', producto=producto)
    except mysql.connector.Error as error:
        print("Error al cargar el producto:", error)
        flash("Error al cargar el producto")
        return redirect(url_for('mostrar_productos'))
    finally:
        cursor.close()
        conexion.close()

# Ruta para procesar el formulario de actualización de producto
@app.route('/actualizar_producto/<int:id>', methods=['POST'])
def actualizar_producto(id):
    conexion = obtener_conexion()
    try:
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        stock_inicial = request.form['stock_inicial']

        cursor = conexion.cursor()
        cursor.execute("UPDATE ProductosItienda SET nombre = %s, descripcion = %s, precio = %s, stock_inicial = %s WHERE id = %s",
                       (nombre, descripcion, precio, stock_inicial, id))
        conexion.commit()

        flash('Producto actualizado correctamente')
        return redirect(url_for('mostrar_productos'))
    except mysql.connector.Error as error:
        print("Error al actualizar el producto:", error)
        flash("Error al actualizar el producto")
        return redirect(url_for('mostrar_formulario_actualizacion', id=id))
    finally:
        cursor.close()
        conexion.close()

# Ruta para eliminar un producto
@app.route('/borrar_producto/<int:id>', methods=['POST'])
def borrar_producto(id):
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM ProductosItienda WHERE id = %s", (id,))
        conexion.commit()

        flash('Producto borrado correctamente')
        return redirect(url_for('mostrar_productos'))
    except mysql.connector.Error as error:
        print("Error al borrar el producto:", error)
        flash("Error al borrar el producto")
        return redirect(url_for('mostrar_productos'))
    finally:
        cursor.close()
        conexion.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
