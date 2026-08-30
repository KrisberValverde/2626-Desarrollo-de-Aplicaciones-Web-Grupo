from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class FacturaForm(FlaskForm):
    cliente = StringField('Nombre Cliente', validators=[
        DataRequired(message="El cliente es obligatorio")
    ])
    producto_id = SelectField('Producto', coerce=int, validators=[
        DataRequired(message="Seleccione un producto")
    ])
    cantidad = IntegerField('Cantidad', validators=[
        DataRequired(message="Obligatorio"),
        NumberRange(min=1, message="Mínimo 1")
    ])
    descuento = FloatField('Descuento %', default=0, validators=[
        NumberRange(min=0, max=100, message="Entre 0 y 100")
    ])
    submit = SubmitField('Generar Factura')
    