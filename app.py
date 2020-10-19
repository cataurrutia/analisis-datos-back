import datetime
import pdmongo as pdm

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
# example /api/?start=2020-02-10&end=2020-07-15
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


@app.route('/json/')
def prueba_json():
    data = request.args.get('data', type=int)

    num = 7
    dic1 = {
        "key1": 10,
        "key2": 1,
        "key3": num
    }

    dic2 = {
        "palabra1": 1,
        "palabra2": 10,
        "palabra3": 25,
        "palabra4": 2,
        "palabra5": 20,
        "palabra6": 30
    }

    dic3 = {
        "value1": 1,
        "value2": 2,
        "value3": 3,
        "value4": 4,
        "value5": 5,
        "value6": 6,
        "value7": 7,
        "value8": 8,
        "value9": 9,
        "value10": 10,
        "value11": 11,
        "value12": 12
    }

    if data == 1:
        return jsonify(dic1)
    elif data == 2:
        return jsonify(dic2)
    elif data == 3:
        return jsonify(dic3)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
