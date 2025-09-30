from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Pedido(db.Model):
    __tablename__ = 'id_pedido'

    id_pedido = db.Column(db.Integer, primary_key=True)
    precio_subtotal = db.Column(db.Numeric(10, 2), nullable=False)
    iva = db.Column(db.Numeric(10, 2), nullable=False)
    precio_final = db.Column(db.Numeric(10, 2), nullable=False)
    metodo_pago = db.Column(db.String(100), nullable=False)
    estado = db.Column(db.String(100), default='pendiente')
    token_carrito = db.Column(db.Boolean, default=False)
    comprobante_url = db.Column(db.Text)
    nombre_asoc_cliente = db.Column(db.String(100))
    telefono_asoc_cliente = db.Column(db.String(100))
    referencia_por = db.Column(db.String(100))
    direccion = db.Column(db.String(250))
    id_usuario = db.Column(db.Integer, nullable=False)
    deleted_at = db.Column(db.DateTime)
    date = db.Column(db.DateTime, default=datetime.now)
    ip = db.Column(db.String(20))

    detalles = db.relationship('DetallePedido', backref='pedido', lazy=True)


class DetallePedido(db.Model):
    __tablename__ = 'pedido_detalle'

    id = db.Column(db.Integer, primary_key=True)
    id_pedido = db.Column(db.Integer, db.ForeignKey('id_pedido.id_pedido'), nullable=False)
    id_producto = db.Column(db.Integer, nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    observacion = db.Column(db.String(250))
    id_usuario = db.Column(db.Integer, nullable=False)
    deleted_at = db.Column(db.DateTime)
    date = db.Column(db.DateTime, default=datetime.now)
    ip = db.Column(db.String(20))