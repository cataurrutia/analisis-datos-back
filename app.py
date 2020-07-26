from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hallo, willkommen!'

@app.route('/api/<int:parametro>')
def llamada(parametro):
    return parametro

if __name__ == '__main__':
    app.run(debug=True, port=5000)
