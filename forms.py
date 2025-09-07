#para mis formularios de Flask-WTF
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, IntegerField,FloatField
from wtforms.validators import DataRequired, Length, Email, number_range, NumberRange, length

class ProductForm(FlaskForm):
        name = StringField ('Producto', validators=[DataRequired(),Length(min=3, max=50)])
        descripcion = StringField('Descripcion')
        precio = FloatField('Precio', validators=[DataRequired(),length(min=1)])
        stock = IntegerField('Cantidad',validators=[DataRequired(),NumberRange(min=3)])

        submit = SubmitField('Agregar Producto')


