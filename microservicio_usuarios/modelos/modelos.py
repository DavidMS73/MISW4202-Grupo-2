import enum

from flask_sqlalchemy import SQLAlchemy
from marshmallow_enum import EnumField
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy import Enum

db = SQLAlchemy()


class RolesEnum(enum.Enum):
    SHOPKEEPER = "SHOPKEEPER"
    SUPER_ADMIN = "SUPER_ADMIN"
    ADMIN = "ADMIN"
    LOGISTIC_DIRECTOR = "LOGISTIC_DIRECTOR"
    LOGISTIC_PERSON = "LOGISTIC_PERSON"
    PROVIDER = "PROVIDER"


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(128))
    usuario = db.Column(db.String(50), unique=True)
    contrasena = db.Column(db.String(50))
    role = db.Column(Enum(RolesEnum), default=RolesEnum.LOGISTIC_PERSON)
    role_hash = db.Column(db.String(512))
    role_assigned_by = db.Column(db.Integer)
    prev_role = db.Column(Enum(RolesEnum), default=RolesEnum.LOGISTIC_PERSON)

class UsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        load_instance = True

    role = EnumField(RolesEnum)
