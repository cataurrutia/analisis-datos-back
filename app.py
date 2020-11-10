import datetime
import pdmongo as pdm
import pandas as pd

from flask import Flask, jsonify, render_template, url_for, request, redirect
from flask_pymongo import PyMongo
from pymongo import MongoClient

MONGO_HOST = 'mongodb://localhost:27017/climateinfo'

# mongodb://167.99.231.117:27017/climateinfo

app = Flask(__name__)
app.config["MONGO_URI"] = MONGO_HOST
mongo = PyMongo(app)


@app.route('/')
def hello_world():
    return render_template('index.html')


# Receiving a range of dates and region
# example /api/?start=2020-09-14&end=2020-09-16&region=5
@app.route('/api/')
def date_range():
    start = request.args.get('start', type=str)
    end = request.args.get('end', type=str)
    region = request.args.get('region', type=int)

    try:
        fecha_inicio = datetime.datetime.strptime(start, "%Y-%m-%d").date().ctime()
        fecha_fin = datetime.datetime.strptime(end, "%Y-%m-%d").date().ctime()

        collection = mongo.db.prepared_tweets
        output = []
        #
        for t in collection.find({'id_region': region}):
            output.append({'tweet': t['tweet'],
                           'fecha': t['fecha'],
                           'location': t['location'],
                           'region': t['id_region']})

        print(type(output))

        for t in collection.find({'created_at': {'$gte': fecha_inicio, '$lt': fecha_fin}}):
            print(t)
            return jsonify({'date': fecha_inicio, 'prepared_tweets': output})


    # return jsonify({'date': fecha_inicio})
    # return jsonify(mongo.db)

    except Exception as e:
        print(e)


# Receiving ONE string date: YYYY-mm-dd
@app.route('/api/<string:fechastr>')
def get_date(fechastr):
    try:
        fecha = datetime.datetime.strptime(fechastr, "%Y-%m-%d").date()
        # hacer algo con fecha
        return fechastr

    except ValueError:
        raise ValueError('{} is not valid date in the format YYYY-MM-DD'.format(fechastr))


# Devuelve json
@app.route('/json/')
def prueba_json():
    data_solicitada = request.args.get('data', type=int)

    data1 = pd.read_csv('csv/dictionaries.csv')
    data2 = pd.read_csv('csv/dictionaries2.csv')
    data3 = pd.read_csv('csv/dictionaries3.csv')

    dict1 = data1.to_json(orient='index')
    dict2 = data2.to_json(orient='index')
    dict3 = data3.to_json(orient='index')

    if data_solicitada == 1:
        return jsonify(dict1)
    elif data_solicitada == 2:
        return jsonify(dict2)
    elif data_solicitada == 3:
        return jsonify(dict3)


# Va a buscar info
def get_twe(**kwargs):
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
