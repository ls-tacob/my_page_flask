from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField
from wtforms.validators import DataRequired, Email
from my_page_flask.bd import obtener_conexion


class UsuarioForm(FlaskForm):
    nombres = StringField('Nombres', validators=[DataRequired()])
    apellidos = StringField('Apellidos', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    activo = SelectField('Estado', choices=[('1', 'Activo'), ('0', 'Inactivo')], validators=[DataRequired()])
    id_rol = SelectField('Rol', coerce=int, validators=[DataRequired()])

    def cargar_roles(self):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT id_rol, descripcion FROM roles")
        roles = cursor.fetchall()
        conexion.close()
        self.id_rol.choices = [(r['id_rol'], r['descripcion']) for r in roles]