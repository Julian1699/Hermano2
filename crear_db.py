from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:123456789@localhost/hermano2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo de Categoría
class Categoria(db.Model):
    __tablename__ = 'Categorias'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    productos = db.relationship('Producto', backref='categoria', lazy=True)

# Modelo de Proveedor
class Proveedor(db.Model):
    __tablename__ = 'Proveedores'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(200), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    productos = db.relationship('Producto', backref='proveedor', lazy=True)

# Modelo de Bodega
class Bodega(db.Model):
    __tablename__ = 'Bodegas'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    ubicacion = db.Column(db.String(200), nullable=False)
    capacidad_maxima = db.Column(db.Integer, nullable=False)
    productos = db.relationship('Producto', backref='bodega', lazy=True)

# Modelo de Producto
class Producto(db.Model):
    __tablename__ = 'Productos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    precio = db.Column(db.Float, nullable=False)
    stock_inicial = db.Column(db.Integer, nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('Categorias.id'), nullable=False)
    proveedor_id = db.Column(db.Integer, db.ForeignKey('Proveedores.id'), nullable=False)
    bodega_id = db.Column(db.Integer, db.ForeignKey('Bodegas.id'), nullable=True)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Base de datos y tablas creadas exitosamente.")
