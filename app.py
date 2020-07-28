from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hallo, willkommen!'

# prueba recibir parametros
@app.route('/api/<int:parametro>')
def llamada(parametro):
    return parametro

@app.route('/<string:nombre>')
def prueba(nombre):
    return 'Hallo '+nombre


if __name__ == '__main__':
    app.run(debug=True, port=5000)
