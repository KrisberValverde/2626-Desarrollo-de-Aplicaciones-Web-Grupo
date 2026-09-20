from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

class FormularioLogin(FlaskForm):
    usuario = StringField('Usuario', validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar Sesión')

class FormularioRegistro(FlaskForm):
    usuario = StringField('Usuario', validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Registrarse')