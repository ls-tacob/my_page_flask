import os
from flask import Flask, render_template, request, redirect, url_for
from product import ProductForm
from flask_bootstrap import Bootstrap5

from my_page_flask.login import LoginForm

app = Flask(__name__)
bootstrap = Bootstrap5(app)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-cambialo-por-favor')

@app.route('/')
def home():
    return render_template('base.html')


from flask import session, redirect, url_for

@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if request.method == 'POST' and login_form.validate_on_submit():
        usuario = login_form.user.data
        session['usuario'] = usuario  # ← Aquí lo guardas
        return redirect(url_for('usuario'))
    return render_template('users/login.html', login_form=login_form)



@app.route('/logout')
def logout():
    session.clear()  # Elimina todos los datos de sesión
    return redirect(url_for('home'))
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
    product_form = ProductForm()
    return render_template('product/product_form.html', product_form=product_form)

if __name__ == '__main__':
    app.run(debug=True)