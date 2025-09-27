from flask import flash, redirect, url_for

from my_page_flask.controladorGlobal import listar_registros_sql, procesar_update_sql
from my_page_flask.bd import obtener_conexion
from my_page_flask.forms.usuarios import UsuarioForm


def listar_usuarios(template_path):
    sql = """
        SELECT us.id_usuario, us.nombres, us.apellidos,
               us.email,
               CASE WHEN us.activo THEN 'ACTIVO' ELSE 'INACTIVO' END AS isActive,
               ro.descripcion AS rol
        FROM usuarios us
        LEFT JOIN roles ro ON us.id_rol = ro.id_rol
    """
    return listar_registros_sql(
        sql_select=sql,
        template_path=template_path,
        context_name='usuarios'
    )




def editar_usuario(id, template_path):
    form = UsuarioForm()

    # Cargar dinámicamente los roles en el combo
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT id_rol, descripcion FROM roles")
    roles = cursor.fetchall()
    form.id_rol.choices = [(r['id_rol'], r['descripcion']) for r in roles]

    def obtener_datos_existentes():
        cursor.execute("""
            SELECT nombres, apellidos, email, activo, id_rol
            FROM usuarios
            WHERE id_usuario = %s
        """, (id,))
        resultado = cursor.fetchone()

        if not resultado:
            flash('Usuario no encontrado')
            return redirect(url_for('vista_usuarios'))

        return {
            'nombres': resultado['nombres'],
            'apellidos': resultado['apellidos'],
            'email': resultado['email'],
            'activo': resultado['activo'],
            'id_rol': resultado['id_rol']
        }

    sql_update = """
        UPDATE usuarios
        SET nombres = %s, apellidos = %s, email = %s, activo = %s, id_rol = %s
        WHERE id_usuario = %s
    """

    return procesar_update_sql(
        form_class=lambda: form,  # para reutilizar el form con roles cargados
        sql_update=sql_update,
        campos_formulario=['nombres', 'apellidos', 'email', 'activo', 'id_rol'],
        obtener_datos_existentes=obtener_datos_existentes,
        template_path=template_path,
        redirect_endpoint='vista_usuarios',
        extras={'id_usuario': id}
    )

