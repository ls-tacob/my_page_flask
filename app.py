import os
from flask import Flask, render_template, request, redirect, url_for
from product import ProductForm
from flask_bootstrap import Bootstrap5
from bd import obtener_conexion
from controlador import procesar_registro, procesar_login

app = Flask(__name__)
bootstrap = Bootstrap5(app)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-cambialo-por-favor')

# Validación institucional al iniciar
conexion = obtener_conexion()
if conexion:
    print("✅ Conexión establecida con la base de datos.")
else:
    print("❌ No se pudo conectar a la base de datos. Verifica configuración.")

@app.route('/')
def home():
    return render_template('base.html')


from flask import session, redirect, url_for

@app.route('/login', methods=['GET', 'POST'])
def login():
    return procesar_login(request)

@app.route('/register', methods=['GET', 'POST'])
def register():
    return procesar_registro(request)  # ✅ Siempre devuelve una respuesta válida

@app.route('/logout')
def logout():
    session.clear()  # Elimina todos los datos de sesión
    return redirect(url_for('home'))


@app.route('/usuario')
def usuario():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    usuario = session['usuario']
    return render_template('admin/usuario.html', usuario=usuario)

@app.route('/about')
def about():
    return render_template('admin/about.html')

@app.route('/contacto')
def contacto():
    return render_template('admin/contacto.html')

@app.route('/producto', methods=['GET', 'POST'])
def producto():
    product_form = ProductForm()
    return render_template('product/product_form.html', product_form=product_form)

if __name__ == '__main__':
    app.run(debug=True)