import datetime

from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')


# Receiving ONE string date: YYYY-mm-dd
@app.route('/api/<string:fechastr>')
def get_date(fechastr):
    try:
        fecha = datetime.datetime.strptime(fechastr, "%Y-%m-%d").date()
        # hacer algo con fecha
        return fechastr

    except ValueError:
        raise ValueError('{} is not valid date in the format YYYY-MM-DD'.format(fecha))


# Receiving a range of dates
# example en local: http://127.0.0.1:5000/api/?start=2020-02-10&end=2020-07-15
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


# Receiving ID de la region
@app.route('/api/<int:id_region>')
def get_region(id_region):
    # filter por region aquí
    return f'parámetro {id_region} recibido'
    # return str(id_region)


def filtro():
    pass


if __name__ == '__main__':
    app.run(debug=True, port=5000)

