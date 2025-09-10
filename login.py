#para mis formularios de Flask-WTF
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, IntegerField,FloatField
from wtforms.validators import DataRequired, Length, Email, number_range, NumberRange, length

class LoginForm(FlaskForm):
        user = StringField ('Usuario', validators=[DataRequired(),Length(min=3, max=20)])
        password = PasswordField('Password', validators=[DataRequired()])

        submit = SubmitField('Iniciar Sesion')


