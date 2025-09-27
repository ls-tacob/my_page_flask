from werkzeug.security import check_password_hash, generate_password_hash
from my_page_flask.bd import obtener_conexion
from my_page_flask.controladorGlobal import procesar_post_sql
from my_page_flask.forms.login import RegisterForm, LoginForm
from flask import render_template, request, redirect, url_for, session, flash
from datetime import datetime, timezone


def obtener_roles():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM roles")
    roles = cursor.fetchall()
    conexion.close()
    return roles

def registrar_usuario():
    password_raw = request.form.get('password')
    if not password_raw:
        flash('La contraseña es obligatoria')
        return render_template('users/register.html', form=RegisterForm())

    extras = {
        'password': generate_password_hash(password_raw),
        'activo': True,
        'date': datetime.now(timezone.utc),
        'ip': request.headers.get('X-Forwarded-For', request.remote_addr)
    }

    return procesar_post_sql(
        form_class=RegisterForm,
        sql_insert="""
            INSERT INTO usuarios (nombres, apellidos, email, celular, password, activo, date, ip)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """,
        campos_formulario=['name', 'last_name', 'email', 'cellphone'],
        template_path='users/register.html',
        redirect_endpoint='usuario',
        extras=extras,
        post_insert_callback=lambda cursor, form, nuevo_id: session.update({
            'usuario': {
                'id': nuevo_id,
                'name': form.name.data,
                'last_name': form.last_name.data,
                'email': form.email.data,
                'rol': 'usuario'
            }
        }),
        context_name='form'
    )


def procesar_login(request):
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.user.data
        password = form.password.data

        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute("""
                SELECT *
                FROM usuarios
                WHERE email = %s
            """, (email,))
            usuario = cursor.fetchone()
            conexion.close()

            print("📦 Datos recibidos:", email, password, usuario)

            if usuario:
                db_password = usuario['password']
                if check_password_hash(db_password, password):
                    session['usuario'] = {
                        'id_usuario': usuario['id_usuario'],
                        'name': usuario['nombres'],
                        'last_name': usuario['apellidos'],
                        'email': usuario['email'],
                        'id_rol': usuario['id_rol']
                    }
                    print("✅ Login exitoso:", session['usuario'])
                    return redirect(url_for('usuario'))
                else:
                    print("❌ Contraseña incorrecta")
            else:
                print("❌ Usuario no encontrado")

        except Exception as e:
            print(f"⚠️ Error en autenticación: {e}")

    return render_template('users/login.html', login_form=form)