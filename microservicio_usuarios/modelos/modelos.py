from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy import Enum
import enum
from marshmallow_enum import EnumField
from sqlalchemy import event
from sqlalchemy.orm.attributes import get_history

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
    type = db.Column(Enum(RolesEnum), default=RolesEnum.LOGISTIC_PERSON)
    hash_type = db.Column(db.String(50))


class UsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        load_instance = True

    type = EnumField(RolesEnum)


def track_status_changes(mapper, connection, target):
    # Get the history of the 'type' attribute
    hist = get_history(target, "type")

    if hist.has_changes():
        print("hi")


# Add the event listeners
event.listen(Usuario, "before_update", track_status_changes)
