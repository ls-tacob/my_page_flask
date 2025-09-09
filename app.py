import os
from flask import Flask, render_template, request, redirect, url_for
from forms import ProductForm

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-cambialo-por-favor')

@app.route('/')
def home():
    return render_template('base.html')

from flask import session

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        password = request.form['password']
        # Validación aquí
        session['usuario'] = usuario
        return redirect(url_for('usuario'))  # o cualquier vista principal
    return render_template('users/login.html')
@app.route('/usuario')
def usuario():
    return render_template('admin/usuario.html')

@app.route('/about')
def about():
    return render_template('admin/about.html')

@app.route('/contacto')
def contacto():
    return render_template('admin/contacto.html')

@app.route('/producto', methods=['GET', 'POST'])
def producto():
    form = ProductForm()
    return render_template('product/form.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)