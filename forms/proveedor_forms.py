from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class ProveedorForm(FlaskForm):
    nombre_empresa = StringField('Nombre Empresa', validators=[
        DataRequired(message="Obligatorio"),
        Length(min=3)
    ])
    ruc = StringField('RUC', validators=[
        DataRequired(message="Obligatorio"),
        Length(min=10, max=13, message="RUC inválido")
    ])
    email = EmailField('Email', validators=[
        DataRequired(),
        Email(message="Email no válido")
    ])
    telefono = StringField('Teléfono', validators=[
        DataRequired(message="Obligatorio")
    ])
    direccion = StringField('Dirección', validators=[
        DataRequired(message="Obligatorio")
    ])
    submit = SubmitField('Guardar Proveedor')
    