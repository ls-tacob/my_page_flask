#para mis formularios de Flask-WTF
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, IntegerField,FloatField
from wtforms.validators import DataRequired, Length, Email, number_range, NumberRange, length

class LoginForm(FlaskForm):
    user = StringField ('Email', validators=[DataRequired(),Length(min=3, max=100)])
    password = PasswordField('Password', validators=[DataRequired()])

    submit = SubmitField('Iniciar Sesion')

class RegisterForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired(), Length(min=3, max=50)])
    last_name = StringField('Apellido', validators=[DataRequired(), Length(min=3, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    cellphone = StringField('Celular', validators=[DataRequired(), Length(min=10, max=10)])
    submit = SubmitField('Registrarse')


