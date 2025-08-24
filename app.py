from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/redirigir-usuario', methods=['POST'])
def usuario_redirect():
    nombre = request.form['nombre']
    return redirect(url_for('usuario', nombre=nombre))

@app.route('/usuario/<string:nombre>')
def usuario(nombre):
    return render_template('admin/usuario.html', nombre=nombre)

@app.route('/about/<string:nombre>')
def about(nombre):
    return render_template('admin/about.html', nombre=nombre)

@app.route('/contacto/<string:nombre>')
def contacto(nombre):
    return render_template('admin/contacto.html', nombre=nombre)

if __name__ == '__main__':
    app.run(debug=True)