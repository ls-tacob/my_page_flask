from collections import OrderedDict
from datetime import datetime
from decimal import Decimal

from flask import request, session, flash, redirect, url_for, render_template
from my_page_flask.controlador.productos import obtener_datos_producto
from my_page_flask.forms.pedido import PedidoForm
from my_page_flask.controladorGlobal import procesar_post_sql  # donde tengas esa función


def registrar_pedido():
    form = PedidoForm()

    if request.method == 'POST' and form.validate_on_submit():
        carrito = session.get('carrito', {})
        id_usuario = session.get('usuario', {}).get('id_usuario')
        if not carrito:
            flash("Tu carrito está vacío", "warning")
            return redirect(url_for('vista_productos'))

        if not id_usuario:
            flash("No se pudo identificar al usuario", "danger")
            return redirect(url_for('login'))

        subtotal = Decimal('0.00')
        resumen = []

        for id_producto, cantidad in carrito.items():
            producto = obtener_datos_producto(id_producto)
            if producto:
                precio = Decimal(str(producto['precio']))
                total_item = precio * cantidad
                subtotal += total_item
                resumen.append({
                    'id': producto['id_producto'],
                    'cantidad': cantidad,
                    'precio': precio,
                    'total': total_item
                })

        iva = round(subtotal * Decimal('0.12'), 2)
        total = round(subtotal + iva, 2)

        sql_insert = """
            INSERT INTO pedidos (
                precio_subtotal, iva, precio_final, metodo_pago,
                estado, id_usuario, date, ip
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        campos_formulario = []  # método de pago ya va en extras

        extras = OrderedDict([
            ('precio_subtotal', subtotal),
            ('iva', iva),
            ('precio_final', total),
            ('metodo_pago', form.metodo_pago.data),
            ('estado', 'pendiente'),
            ('id_usuario', id_usuario),  # ✅ corregido aquí
            ('date', datetime.now()),
            ('ip', request.remote_addr)
        ])

        def post_insert_callback(cursor, form, nuevo_id):
            for item in resumen:
                cursor.execute("""
                    INSERT INTO pedido_detalle (
                        id_pedido, id_producto, cantidad,
                        observacion, id_usuario, date, ip
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (
                    nuevo_id, item['id'], item['cantidad'],
                    '', id_usuario,
                    datetime.now(), request.remote_addr
                ))
            session.pop('carrito', None)

        return procesar_post_sql(
            form_class=PedidoForm,
            sql_insert=sql_insert,
            campos_formulario=campos_formulario,
            template_path='users/pago.html',
            redirect_endpoint='vista_confirmacion_pedido',
            extras=extras,
            post_insert_callback=post_insert_callback
        )

    # Renderizar pago.html si no se hizo POST válido
    carrito = session.get('carrito', {})
    resumen = []
    subtotal = Decimal('0.00')

    for id_producto, cantidad in carrito.items():
        producto = obtener_datos_producto(id_producto)
        if producto:
            precio = Decimal(str(producto['precio']))
            total_item = precio * cantidad
            subtotal += total_item
            resumen.append({
                'id': producto['id_producto'],
                'nombre': producto['nombre'],
                'imagen': producto['imagen'],
                'cantidad': cantidad,
                'precio': precio,
                'total': total_item
            })

    iva = round(subtotal * Decimal('0.12'), 2)
    total = round(subtotal + iva, 2)

    return render_template('users/pago.html', form=form, resumen=resumen, subtotal=subtotal, iva=iva, total=total)
