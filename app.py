import os

from flask import Flask, render_template, request, redirect, url_for

from forms import ProductForm

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-cambialo-por-favor')


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Aquí irá la lógica de autenticación
        usuario = request.form['usuario']
        password = request.form['password']
        # Validar usuario y contraseña


@app.route('/usuario/<string:nombre>')
def usuario(nombre):
    return render_template('admin/usuario.html', nombre=nombre)

@app.route('/about/<string:nombre>')
def about(nombre):
    return render_template('admin/about.html', nombre=nombre)

@app.route('/contacto/<string:nombre>')
def contacto(nombre):
    return render_template('admin/contacto.html', nombre=nombre)

@app.route('/producto/<string:nombre>', methods=['GET', 'POST'])
def producto(nombre):
    form = ProductForm()  # asegúrate de tener: from forms import ProductForm
    return render_template('product/form.html', form=form, nombre=nombre)

if __name__ == '__main__':
    app.run(debug=True)