import os
from flask import Flask, render_template, request, session, redirect, url_for
from flask_bootstrap import Bootstrap5
from bd import obtener_conexion
from my_page_flask.forms.product import ProductForm
from my_page_flask.controlador.login import procesar_login, registrar_usuario
from my_page_flask.controlador.productos import registrar_producto
from my_page_flask.controlador.usuarios import listar_usuarios, editar_usuario

from functools import wraps

app = Flask(__name__)
bootstrap = Bootstrap5(app)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'Le0messi10%-GOAT')

# ✅ Decorador institucional para validar sesión
def login_requerido(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'usuario' not in session:
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return wrapper

# ✅ Validación institucional al iniciar
conexion = obtener_conexion()
if conexion:
    print("✅ Conexión establecida con bdd.")
else:
    print("❌ No se pudo conectar a la base de datos. Verifica configuración.")

@app.route('/')
def home():
    return render_template('base.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return procesar_login(request)

@app.route('/register', methods=['GET', 'POST'])
def register():
    return registrar_usuario()

@app.route('/logout')
def logout():
    session.clear()  # Elimina todos los datos de sesión
    return redirect(url_for('home'))

@app.route('/usuario')
@login_requerido
def usuario():
    return render_template('admin/usuario.html', usuario=session['usuario'])

@app.route('/about')
@login_requerido
def about():
    return render_template('admin/about.html')

@app.route('/contacto')
@login_requerido
def contacto():
    return render_template('admin/contacto.html')

@app.route('/producto', methods=['GET', 'POST'])
@login_requerido
def producto():
    return registrar_producto()

@app.route('/usuarios')
@login_requerido
def vista_usuarios():
    return listar_usuarios('admin/usuarios.html')

@app.route('/usuarios/editar/<int:id>', methods=['GET', 'POST'])
@login_requerido
def vista_editar_usuario(id):
    return editar_usuario(id, 'admin/editar_usuario.html')

if __name__ == '__main__':
    app.run(debug=True)