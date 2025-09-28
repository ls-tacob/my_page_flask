import sqlite3

from flask import request, session, redirect, url_for, render_template, flash
from datetime import datetime
from my_page_flask.bd import obtener_conexion


def procesar_post_sql(
    form_class,
    sql_insert,
    campos_formulario,
    template_path,
    redirect_endpoint,
    extras=None,
    post_insert_callback=None,
    context_name='form'
):
    form = form_class()

    if request.method == 'POST' and form.validate_on_submit():
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()

            datos = [getattr(form, campo).data for campo in campos_formulario]

            if extras:
                datos.extend(extras.values())

            cursor.execute(sql_insert, tuple(datos))
            nuevo_id = cursor.lastrowid

            if post_insert_callback:
                post_insert_callback(cursor, form, nuevo_id)

            conexion.commit()
            conexion.close()

            flash('Registro exitoso')
            return redirect(url_for(redirect_endpoint))

        except Exception as e:
            print(f"❌ Error al procesar POST genérico: {e}")
            flash('Ocurrió un error al registrar')
            return render_template(template_path, **{context_name: form})

    return render_template(template_path, **{context_name: form})


def listar_registros_sql(sql_select, template_path, context_name='registros'):
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()  # DictCursor ya está configurado en la conexión

        cursor.execute(sql_select)
        registros = cursor.fetchall()

        conexion.close()
        return render_template(template_path, **{context_name: registros})

    except Exception as e:
        print(f"❌ Error al listar registros: {e}")
        flash('Ocurrió un error al cargar los datos')
        return render_template(template_path, **{context_name: []})

def procesar_update_sql(
    form_class,
    sql_update,
    campos_formulario,
    obtener_datos_existentes,
    template_path,
    redirect_endpoint,
    extras=None,
    post_update_callback=None,
    context_name='form',
    context_extra=None  # 👈 nuevo parámetro
):
    form = form_class()

    if request.method == 'POST' and form.validate_on_submit():
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()

            datos = [getattr(form, campo).data for campo in campos_formulario]

            if extras:
                datos.extend(extras.values())

            cursor.execute(sql_update, tuple(datos))

            if post_update_callback:
                post_update_callback(cursor, form)

            conexion.commit()
            conexion.close()

            flash('Actualización exitosa')
            return redirect(url_for(redirect_endpoint))

        except Exception as e:
            print(f"❌ Error al actualizar: {e}")
            flash('Ocurrió un error al actualizar')
            return render_template(template_path, **{context_name: form})

    # GET: precargar datos
    datos_existentes = obtener_datos_existentes()
    for campo in campos_formulario:
        setattr(getattr(form, campo), 'data', datos_existentes.get(campo))

    return render_template(template_path, **{
        context_name: form,
        **(context_extra or {})
    })

def procesar_delete_sql(sql_delete, redirect_endpoint, extras=None, post_delete_callback=None):
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        # Agregar marca de tiempo actual como delete_at
        delete_at = datetime.now()
        datos = [delete_at] + list(extras.values()) if extras else [delete_at]

        cursor.execute(sql_delete, tuple(datos))

        if post_delete_callback:
            post_delete_callback(cursor)

        conexion.commit()
        conexion.close()

        flash('Usuario marcado como eliminado', 'success')  # ✅ Alerta institucional
        return redirect(url_for(redirect_endpoint))

    except Exception as e:
        print(f"❌ Error al eliminar: {e}")
        flash('Ocurrió un error al eliminar el usuario', 'danger')  # ❌ Alerta institucional
        return redirect(url_for(redirect_endpoint))
