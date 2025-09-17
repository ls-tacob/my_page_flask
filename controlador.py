from werkzeug.security import check_password_hash, generate_password_hash
from bd import obtener_conexion
from login import RegisterForm, LoginForm
from flask import render_template, request, redirect, url_for, session

def obtener_roles():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM roles")
    roles = cursor.fetchall()
    conexion.close()
    return roles

def procesar_registro(request):
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        print("📦 Formulario completo:", form.data)
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()

            password_segura = generate_password_hash(form.password.data)

            cursor.execute("""
                INSERT INTO usuarios (nombres, apellidos, email, celular, password)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                form.name.data,
                form.last_name.data,
                form.email.data,
                form.cellphone.data,
                password_segura
            ))

            nuevo_id = cursor.lastrowid  # ✅ ID generado
            rol_asignado = 'usuario'     # ✅ Rol por defecto (puedes consultar roles si lo deseas)

            conexion.commit()
            conexion.close()

            session['usuario'] = {
                'id': nuevo_id,
                'name': form.name.data,
                'last_name': form.last_name.data,
                'email': form.email.data,
                'rol': rol_asignado
            }

            return redirect(url_for('usuario'))

        except Exception as e:
            print(f"❌ Error al registrar usuario: {e}")
            return render_template('users/register.html', register_form=form)

    return render_template('users/register.html', register_form=form)

def procesar_login(request):
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.user.data
        password = form.password.data

        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute("""
                SELECT id_usuario, nombres, apellidos, email, password
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
                        'email': usuario['email']
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