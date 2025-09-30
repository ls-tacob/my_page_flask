import os
from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from bd import obtener_conexion
from my_page_flask.controlador.pedidos import registrar_pedido
from my_page_flask.forms.product import ProductForm
from my_page_flask.controlador.login import procesar_login, registrar_usuario
from my_page_flask.controlador.productos import registrar_producto, listar_productos, editar_producto, \
    eliminar_producto, obtener_productos_disponibles, obtener_datos_producto
from my_page_flask.controlador.usuarios import listar_usuarios, editar_usuario, eliminar_usuario
from functools import wraps
from decimal import Decimal

from my_page_flask.models import Pedido, DetallePedido

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

@app.route('/tienda')
@login_requerido
def tienda():
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


@app.route('/comprar', methods=['GET', 'POST'])
def comprar():
    origen = request.args.get('origen') or request.form.get('origen')
    metodo_pago = request.args.get('metodo_pago') or request.form.get('metodo_pago')
    id_producto = request.args.get('id_producto') or request.form.get('id_producto')
    cantidad = int(request.args.get('cantidad', 1) or request.form.get('cantidad', 1))

    if origen == 'directo':
        session['carrito'] = {id_producto: cantidad}

    session['metodo_pago'] = metodo_pago
    return redirect(url_for('registrar_pedido_view'))


@app.route('/agregar-carrito', methods=['POST'])
def agregar_al_carrito():
    id_producto = request.form.get('id_producto')
    cantidad = int(request.form.get('cantidad', 1))

    if not id_producto:
        flash("Producto inválido", "danger")
        return redirect(url_for('tienda'))

    carrito = session.get('carrito', {})
    carrito[id_producto] = carrito.get(id_producto, 0) + cantidad
    session['carrito'] = carrito

    flash("Producto agregado al carrito", "success")
    return redirect(url_for('tienda'))

@app.route('/carrito', methods=['GET'])
def vista_carrito():
    carrito = session.get('carrito', {})
    resumen = []
    subtotal = 0

    for id_producto, cantidad in carrito.items():
        producto = obtener_datos_producto(id_producto)

        if producto and isinstance(producto, dict):
            total_item = producto['precio'] * cantidad
            subtotal += total_item
            resumen.append({
                'id': producto['id_producto'],
                'nombre': producto['nombre'],
                'precio': producto['precio'],
                'imagen': producto['imagen'],
                'cantidad': cantidad,
                'total': total_item
            })

    print(f"🧪 Resumen del carrito: {resumen}")

    iva = round(subtotal * Decimal('0.12'), 2)
    total = round(subtotal + iva, 2)

    return render_template(
        'users/carrito.html',
        resumen=resumen,
        subtotal=subtotal,
        iva=iva,
        total=total
    )

@app.route('/cancelar-pedido', methods=['POST'])
def cancelar_pedido():
    session.pop('carrito', None)
    flash("Pedido cancelado correctamente", "warning")
    return redirect(url_for('tienda'))  # o donde quieras redirigir

@app.route('/pedido-confirmado/<int:pedido_id>', endpoint='vista_confirmacion_pedido')
def vista_confirmacion_pedido(pedido_id):
    pedido = Pedido.query.filter_by(id_pedido=pedido_id).first_or_404()
    detalles = DetallePedido.query.filter_by(id_pedido=pedido_id).all()
    return render_template('users/confirmacion.html', pedido=pedido, detalles=detalles)

@app.route('/registrar-pedido', methods=['POST'])
def registrar_pedido_view():
    return registrar_pedido()

if __name__ == '__main__':
    app.run(debug=True)