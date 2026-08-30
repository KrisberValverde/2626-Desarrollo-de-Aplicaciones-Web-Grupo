from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length

class ProductoForm(FlaskForm):
    nombre = StringField('Nombre del Producto', validators=[
        DataRequired(message="El nombre es obligatorio"),
        Length(min=3, max=100, message="Mínimo 3 caracteres")
    ])
    precio = FloatField('Precio', validators=[
        DataRequired(message="El precio es obligatorio"),
        NumberRange(min=0.01, message="El precio debe ser mayor a 0")
    ])
    categoria = SelectField('Categoría', choices=[
        ('', 'Seleccione una categoría'),
        ('Ropa', 'Ropa'),
        ('Abrigos', 'Abrigos'),
        ('Vestidos', 'Vestidos'),
        ('Tops', 'Tops'),
        ('Pantalones', 'Pantalones'),
        ('Accesorios', 'Accesorios')
    ], validators=[DataRequired(message="Seleccione una categoría")])
    stock = IntegerField('Stock', validators=[
        DataRequired(message="El stock es obligatorio"),
        NumberRange(min=0, message="No puede ser negativo")
    ])
    imagen = StringField('URL Imagen', validators=[
        DataRequired(message="La imagen es obligatoria")
    ])
    submit = SubmitField('Guardar Producto')