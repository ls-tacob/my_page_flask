# sql dice
from flask_sqlalchemy import SQLAlchemy
db= SQLAlchemy
class Producto (db.model):
    id_producto=db.Column(db.Integer, primary_key=True)
    nombre =db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.String(50), nullable= True)
    precio = db.Column(db.Decimal(10,2), nullable=False)
    stock = db.Column(db.integer,nullable=False)

    def __repr__(self):
        return f'<Producto {self.nombre}'

