from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/usuario/<string:nombre>')
def usuario(nombre):
    nombre_limpio = nombre.strip().capitalize()
    return render_template('admin/usuario.html', nombre=nombre_limpio)



if __name__ == '__main__':
    app.run(debug=True)
