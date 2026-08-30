from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class ClienteForm(FlaskForm):
    nombre = StringField('Nombre Completo', validators=[
        DataRequired(message="Obligatorio"),
        Length(min=3, message="Mínimo 3 caracteres")
    ])
    correo = EmailField('Correo Electrónico', validators=[
        DataRequired(message="Obligatorio"),
        Email(message="Ingrese un correo válido")
    ])
    telefono = StringField('Teléfono', validators=[
        DataRequired(message="Obligatorio"),
        Length(min=10, max=10, message="Debe tener 10 dígitos")
    ])
    submit = SubmitField('Guardar Cliente')
