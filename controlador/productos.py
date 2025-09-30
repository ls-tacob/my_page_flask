import os
from datetime import datetime, timezone
from flask import request, session, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
from my_page_flask.forms.product import ProductForm
from my_page_flask.controladorGlobal import procesar_post_sql, listar_registros_sql, procesar_update_sql, procesar_delete_sql
from my_page_flask.bd import obtener_conexion


UPLOAD_FOLDER = 'static/uploads/producto'

def registrar_producto(template_path):
    form = ProductForm()

    if request.method == 'POST' and form.validate_on_submit():
        imagen = form.imagen.data
        nombre_archivo = secure_filename(imagen.filename)
        ruta_imagen = os.path.join(UPLOAD_FOLDER, nombre_archivo)
        imagen.save(ruta_imagen)

        extras = {
            'id_usuario': session.get('usuario', {}).get('id_usuario'),
            'timestamp': datetime.now(timezone.utc),
            'ip': request.headers.get('X-Forwarded-For', request.remote_addr),
            'imagen': nombre_archivo
        }

        return procesar_post_sql(
            form_class=lambda: form,
            sql_insert="""
                INSERT INTO producto (nombre, descripcion, precio, stock, id_usuario, date, ip, imagen)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            campos_formulario=['nombre', 'descripcion', 'precio', 'stock'],
            template_path=template_path,
            redirect_endpoint='producto',
            extras=extras,
            post_insert_callback=None,
            context_name='form'
        )

    # GET o formulario inválido
    return render_template(template_path, form=form)

def listar_productos(template_path):
    sql = """
        SELECT id_producto, nombre, descripcion, precio, stock    
        FROM producto 
        WHERE delete_at IS NULL
    """
    return listar_registros_sql(
        sql_select=sql,
        template_path=template_path,
        context_name='productos'
    )
def obtener_productos_disponibles():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT id_producto, nombre, descripcion, precio, stock, imagen
        FROM producto
        WHERE delete_at IS NULL AND stock > 0
        ORDER BY date DESC
    """)
    return cursor.fetchall()


def editar_producto(id, template_path):
    form = ProductForm()

    def obtener_datos_existentes():
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT nombre, descripcion, precio, stock, imagen
            FROM producto
            WHERE id_producto = %s AND delete_at IS NULL
        """, (id,))
        resultado = cursor.fetchone()

        if not resultado:
            flash('Producto no encontrado', 'danger')
            return redirect(url_for('vista_productos'))

        return {
            'nombre': resultado['nombre'],
            'descripcion': resultado['descripcion'],
            'precio': resultado['precio'],
            'stock': resultado['stock'],
            'imagen': resultado['imagen']
        }

    sql_update = """
        UPDATE producto
        SET nombre = %s, descripcion = %s, precio = %s, stock = %s, date = %s, ip = %s, id_usuario = %s
        WHERE id_producto = %s
    """

    extras = {
        'date': datetime.now(),
        'ip': request.headers.get('X-Forwarded-For', request.remote_addr),
        'id_usuario': session.get('usuario', {}).get('id_usuario'),
        'id_producto': id
    }

    # ⚠️ Solo si es GET, obtenemos datos para pasarlos como contexto_extra
    context_extra = {}
    if request.method == 'GET':
        datos_existentes = obtener_datos_existentes()
        context_extra = {'producto': datos_existentes}

    return procesar_update_sql(
        form_class=lambda: form,
        sql_update=sql_update,
        campos_formulario=['nombre', 'descripcion', 'precio', 'stock'],
        obtener_datos_existentes=obtener_datos_existentes,
        template_path=template_path,
        redirect_endpoint='vista_productos',
        extras=extras,
        context_extra=context_extra  # ✅ ahora sí está definido correctamente
    )

def eliminar_producto(id):
    sql_delete = """
        UPDATE producto
        SET delete_at = %s, id_usuario = %s, date = %s,ip = %s
        WHERE id_producto = %s
    """

    # ⚠️ Orden explícito de parámetros según el SQL
    extras = {
        'id_usuario': session.get('usuario', {}).get('id_usuario'),
        'date': datetime.now(),
        'ip': request.remote_addr,
        'id_producto': id
    }

    return procesar_delete_sql(
        sql_delete=sql_delete,
        redirect_endpoint='vista_productos',
        extras=extras
    )

def obtener_productos(origen):
    """
    Extrae productos desde sesión (carrito) o desde request (compra directa).
    Retorna una lista de diccionarios con id_producto y cantidad.
    """
    productos = []

    if origen == 'carrito':
        carrito = session.get('carrito', {})
        for id_producto, cantidad in carrito.items():
            productos.append({
                'id_producto': int(id_producto),
                'cantidad': int(cantidad)
            })
    elif origen == 'directo':
        id_producto = request.form.get('id_producto')
        cantidad = request.form.get('cantidad', 1)
        productos.append({
            'id_producto': int(id_producto),
            'cantidad': int(cantidad)
        })

    return productos


def obtener_datos_producto(id_producto):
    """
    Retorna los datos de un producto específico como dict.
    Compatible con cursor tipo DictCursor.
    """
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        sql = """
            SELECT id_producto, nombre, descripcion, precio, stock, imagen
            FROM producto
            WHERE delete_at IS NULL AND id_producto = %s
        """
        cursor.execute(sql, (id_producto,))
        resultado = cursor.fetchone()
        conexion.close()

        if resultado is None:
            raise ValueError(f"Producto con ID {id_producto} no encontrado")

        return {
            'id_producto': resultado['id_producto'],
            'nombre': resultado['nombre'],
            'descripcion': resultado['descripcion'],
            'precio': resultado['precio'],
            'stock': resultado['stock'],
            'imagen': resultado['imagen']
        }

    except Exception as e:
        print(f"❌ Error al obtener datos del producto {id_producto}: {type(e).__name__} → {e}")
        return {
            'id_producto': id_producto,
            'nombre': 'Error',
            'descripcion': '',
            'precio': 0.00,
            'stock': 0,
            'imagen': ''
        }