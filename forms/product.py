from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange
from flask_wtf.file import FileField, FileAllowed, FileRequired

class ProductForm(FlaskForm):
    nombre = StringField('Producto', validators=[
        DataRequired(),
        Length(min=3, max=50)
    ])
    descripcion = StringField('Descripción')
    precio = DecimalField('Precio', validators=[
        DataRequired(),
        NumberRange(min=0.01, message="El precio debe ser mayor a cero")
    ])
    stock = IntegerField('Cantidad', validators=[
        DataRequired(),
        NumberRange(min=3)
    ])
    imagen = FileField('Imagen del producto', validators=[
        FileRequired(message="Debes subir una imagen"),
        FileAllowed(['jpg', 'jpeg', 'png', 'webp'], 'Solo se permiten imágenes')
    ])
    submit = SubmitField('Agregar Producto')