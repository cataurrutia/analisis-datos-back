from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hallo, willkommen!'

# prueba recibir parametros
# http://http//167.99.231.117:5000/api/llamada?parametro=1000
@app.route('/api/<int:parametro>')
def llamada(parametro):
    respuesta_modelo = subprocess.call('python3 tutorial2.py', parametro)
    #return (data:{var1:'valor1', var2:'valor2'})
    return parametro

@app.route('/<string:nombre>')
def prueba(nombre):
    return 'Hallo '+nombre


if __name__ == '__main__':
    app.run(debug=True, port=5000)
