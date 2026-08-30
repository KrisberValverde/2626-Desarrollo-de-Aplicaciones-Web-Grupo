from .producto_forms import ProductoForm
from .cliente_forms import ClienteForm
from .factura_forms import FacturaForm
from .proveedor_forms import ProveedorForm

from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class ContactoForm(FlaskForm):
    nombre = StringField('Nombre', validators=[
        DataRequired(message="Obligatorio"),
        Length(min=2, message="Mínimo 2 caracteres")
    ])
    correo = EmailField('Correo', validators=[
        DataRequired(message="Obligatorio"),
        Email(message="Correo no válido")
    ])
    mensaje = TextAreaField('Mensaje', validators=[
        DataRequired(message="Obligatorio"),
        Length(min=10, message="Mínimo 10 caracteres")
    ])
    submit = SubmitField('Enviar Mensaje')

