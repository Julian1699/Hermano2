from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:123456789@localhost/hermano2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo de Producto
class Producto(db.Model):
    __tablename__ = 'ProductosItienda'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    precio = db.Column(db.Float, nullable=False)
    stock_inicial = db.Column(db.Integer, nullable=False)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Base de datos y tablas creadas exitosamente.")
