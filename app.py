import datetime

from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')


# prueba recibir parametros
# http://http//167.99.231.117:5000/api/llamada?parametro=1000
@app.route('/api/<int:parametro>')
def llamada(parametro):
    respuesta_modelo = subprocess.call('python3 tutorial2.py', parametro)
    # return (data:{var1:'valor1', var2:'valor2'})
    return parametro


# Receiving ONE date YYYY-mm-dd, in str
@app.route('/api/<string:fechastr>')
def get_date(fechastr):
    try:
        fecha = datetime.datetime.strptime(fechastr, "%Y-%m-%d").date()
        return fecha

    except ValueError:
        raise ValueError('{} is not valid date in the format YYYY-MM-DD'.format(fecha))


# Receiving a range of dates, example: http://127.0.0.1:5000/api/?start=2020-02-10&end=2020-07-15
@app.route('/api/')
def date_range():
    start = request.args.get('start', type=str)
    end = request.args.get('end', type=str)

    try:
        fecha_inicio = datetime.datetime.strptime(start, "%Y-%m-%d").date()
        fecha_fin = datetime.datetime.strptime(end, "%Y-%m-%d").date()
        print(fecha_inicio)
        print(fecha_fin)
        return render_template('index.html', fecha_inicio=fecha_inicio, fecha_fin=fecha_fin)

    except Exception as e:
        print(e)
        # raise ValueError('{} is not valid date in the format YYYY-MM-DD'.format(fecha))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
