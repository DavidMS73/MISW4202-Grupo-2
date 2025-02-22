from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()

productos_compras = db.Table(
    "producto_compra",
    db.Column(
        "producto_id", db.Integer, db.ForeignKey("producto.id"), primary_key=True
    ),
    db.Column("compra_id", db.Integer, db.ForeignKey("compra.id"), primary_key=True),
)


class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(128))
    descripcion = db.Column(db.String(512))
    condiciones_almacenamiento = db.Column(db.String(512))
    valor_unidad = db.Column(db.Integer)
    compras = db.relationship(
        "Compra", secondary="producto_compra", back_populates="productos"
    )


class Compra(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    estado = db.Column(db.String(128))
    fecha_creacion = db.Column(db.Date)
    productos = db.relationship(
        "Producto", secondary="producto_compra", back_populates="compras"
    )


class ProductoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Producto
        include_relationships = True
        load_instance = True


class CompraSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Compra
        include_relationships = True
        load_instance = True
