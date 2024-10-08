from enum import Enum
from app import db
from datetime import datetime

class TransaccionTipo(Enum):
    ENTRADA = 1
    SALIDA = 2

class Stock(db.Model):
    __tablename__ = "stock"
    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, nullable=False)
    cantidad = db.Column(db.Float, nullable=False)
    fecha_transaccion = db.Column(db.DateTime, default=datetime.utcnow)
    entrada_salida = db.Column(db.Enum(TransaccionTipo), nullable=False)

    @staticmethod
    def agregar_stock(producto_id, cantidad):
        nuevo_stock = Stock(producto_id=producto_id, cantidad=cantidad, entrada_salida=TransaccionTipo.ENTRADA)
        db.session.add(nuevo_stock)
        db.session.commit()
        return nuevo_stock

    @staticmethod
    def retirar_producto(producto_id, cantidad):
        nuevo_stock = Stock(producto_id=producto_id, cantidad=cantidad, entrada_salida=TransaccionTipo.SALIDA)
        db.session.add(nuevo_stock)
        db.session.commit()
        return nuevo_stock
