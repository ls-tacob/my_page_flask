from werkzeug.security import check_password_hash, generate_password_hash
from my_page_flask.bd import obtener_conexion
from my_page_flask.controladorGlobal import procesar_post_sql
from my_page_flask.forms.product import ProductForm
from flask import render_template, request, redirect, url_for, session
from datetime import datetime, timezone

def obtener_productos():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM producto")
    productos = cursor.fetchall()
    conexion.close()
    return productos

def registrar_producto():
    extras = {
        'id_usuario': session.get('usuario', {}).get('id_usuario'),
        'timestamp': datetime.now(timezone.utc),
        'ip': request.headers.get('X-Forwarded-For', request.remote_addr)
    }

    return procesar_post_sql(
        form_class=ProductForm,
        sql_insert="""
            INSERT INTO producto (nombre, descripcion, precio, stock, id_usuario, date, ip)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,
        campos_formulario=['nombre', 'descripcion', 'precio', 'stock'],
        template_path='product/product_form.html',
        redirect_endpoint='producto',
        extras=extras,
        post_insert_callback=None,
        context_name='form'
    )
