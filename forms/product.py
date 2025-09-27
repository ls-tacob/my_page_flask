#para mis formularios de Flask-WTF
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, IntegerField,FloatField
from wtforms.fields.numeric import DecimalField
from wtforms.validators import DataRequired, Length, Email, number_range, NumberRange, length

class ProductForm(FlaskForm):
        nombre = StringField ('Producto', validators=[DataRequired(),Length(min=3, max=50)])
        descripcion = StringField('Descripcion')
        precio = DecimalField('Precio', validators=[
            DataRequired(),
            NumberRange(min=0.01, message="El precio debe ser mayor a cero")
        ])
        stock = IntegerField('Cantidad',validators=[DataRequired(),NumberRange(min=3)])

        submit = SubmitField('Agregar Producto')


