import os
from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from bd import obtener_conexion
from my_page_flask.forms.product import ProductForm
from my_page_flask.controlador.login import procesar_login, registrar_usuario
from my_page_flask.controlador.productos import registrar_producto, listar_productos, editar_producto, eliminar_producto, obtener_productos_disponibles
from my_page_flask.controlador.usuarios import listar_usuarios, editar_usuario, eliminar_usuario
from functools import wraps

app = Flask(__name__)
bootstrap = Bootstrap5(app)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'Le0messi10%-GOAT')

# ✅ Decorador institucional para validar sesión
def login_requerido(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'usuario' not in session:
            flash('Debes iniciar sesión para acceder a esta sección', 'warning')
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return wrapper

# ✅ Validación institucional al iniciar
conexion = obtener_conexion()
if conexion:
    print("✅ Conexión establecida con bdd.")
else:
    print("❌ No se pudo conectar a la base de datos. Verifica configuración.")

# ✅ Función institucional para lanzar alertas por tipo de acción
def alerta_accion(tipo, entidad, id=None, nombre=None):
    if tipo == 'editar':
        mensaje = f'Estás editando {entidad}'
        if nombre:
            mensaje += f': {nombre}'
        elif id:
            mensaje += f' con ID {id}'
        flash(mensaje, 'success')
    elif tipo == 'crear':
        flash(f'{entidad.capitalize()} creado correctamente', 'success')
    elif tipo == 'eliminar':
        flash(f'{entidad.capitalize()} eliminado correctamente', 'success')
    elif tipo == 'error':
        flash(f'Ocurrió un error al procesar {entidad}', 'danger')
    elif tipo == 'info':
        flash(f'{entidad.capitalize()}', 'info')

# ✅ Rutas institucionales
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
    session.clear()
    flash('Sesión cerrada correctamente', 'info')
    return redirect(url_for('home'))

@app.route('/usuario')
@login_requerido
def usuario():
    productos = obtener_productos_disponibles()  # 👈 función que filtra delete_at IS NULL y stock > 0
    return render_template('users/usuario.html', usuario=session['usuario'], productos=productos)

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
    return registrar_producto('product/product_form.html')

@app.route('/usuarios')
@login_requerido
def vista_usuarios():
    return listar_usuarios('admin/usuarios.html')

@app.route('/usuarios/editar/<int:id>', methods=['GET', 'POST'])
@login_requerido
def vista_editar_usuario(id):
    return editar_usuario(id, 'admin/editar_usuario.html')

@app.route('/usuarios/eliminar/<int:id>', methods=['POST'])
@login_requerido
def vista_eliminar_usuario(id):
    return eliminar_usuario(id)

@app.route('/productos')
@login_requerido
def vista_productos():
    return listar_productos('product/productos.html')

@app.route('/productos/editar/<int:id>', methods=['GET', 'POST'])
@login_requerido
def vista_editar_producto(id):
    return editar_producto(id, 'product/editar_producto.html')


@app.route('/productos/eliminar/<int:id>', methods=['POST'])
@login_requerido
def vista_eliminar_producto(id):
    return eliminar_producto(id)

if __name__ == '__main__':
    app.run(debug=True)