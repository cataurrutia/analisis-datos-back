import datetime
import pdmongo as pdm

from flask import Flask, render_template, url_for, request, redirect
from pymongo import MongoClient

app = Flask(__name__)
MONGO_HOST = 'mongodb://localhost/twitterdb'
date_search = []


@app.route('/')
def hello_world():
    return render_template('index.html')


# Receiving a range of dates and region
# example /api/?start=2020-02-10&end=2020-07-15
# example /api/?start=2020-09-14&end=2020-09-16&region=5
@app.route('/api/')
def date_range():
    start = request.args.get('start', type=str)
    end = request.args.get('end', type=str)
    region = request.args.get('region', type=int)

    try:
        fecha_inicio = datetime.datetime.strptime(start, "%Y-%m-%d").date()
        fecha_fin = datetime.datetime.strptime(end, "%Y-%m-%d").date()
        print(fecha_inicio)
        print(fecha_fin)
        print(region)
        return render_template('index.html', fecha_inicio=fecha_inicio, fecha_fin=fecha_fin, region=region)

    except Exception as e:
        print(e)
        # raise ValueError('{} is not valid date in the format YYYY-MM-DD'.format(fecha))


# Receiving ONE string date: YYYY-mm-dd
@app.route('/api/<string:fechastr>')
def get_date(fechastr):
    try:
        fecha = datetime.datetime.strptime(fechastr, "%Y-%m-%d").date()
        # hacer algo con fecha
        return fechastr

    except ValueError:
        raise ValueError('{} is not valid date in the format YYYY-MM-DD'.format(fechastr))


# Receiving ID de la region
@app.route('/api/<int:id_region>')
def get_region(id_region):
    # filter por region aquí
    return f'parámetro {id_region} recibido'
    # return str(id_region)


def get_tweets(**kwargs):
    client = MongoClient(MONGO_HOST)
    db = client.climateinfo
    col = db.filtered_stream
    region = ''
    fecha_ini = ''
    fecha_fin = ''

    query = {"created_at": fecha_ini}
    query_region = {"region": region}

    pass


if __name__ == '__main__':
    app.run(debug=True, port=5000)
