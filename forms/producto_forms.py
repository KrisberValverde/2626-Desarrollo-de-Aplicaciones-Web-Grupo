from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class ProductoForm(FlaskForm):
    nombre = StringField('Nombre del Producto', validators=[DataRequired()])
    categoria = SelectField(
        'Categoría',
        choices=[
            ('Vestidos', 'Vestidos'),
            ('Tops', 'Tops'),
            ('Pantalones', 'Pantalones'),
            ('Camisas', 'Camisas'),
            ('Enterizos', 'Enterizos'),
            ('Faldas', 'Faldas')
        ],
        validators=[DataRequired()]
    )
    precio = DecimalField('Precio ($)', validators=[DataRequired(), NumberRange(min=0.01)])
    stock_s = IntegerField('Stock Talla S', default=0, validators=[NumberRange(min=0)])
    stock_m = IntegerField('Stock Talla M', default=0, validators=[NumberRange(min=0)])
    stock_l = IntegerField('Stock Talla L', default=0, validators=[NumberRange(min=0)])

    imagen = StringField('URL de la Imagen', validators=[DataRequired()])
    submit = SubmitField('Guardar Producto')