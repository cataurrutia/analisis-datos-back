import datetime
import pdmongo as pdm

from flask import Flask, jsonify, render_template, url_for, request, redirect
from flask_pymongo import PyMongo

MONGO_HOST = 'mongodb://localhost:27017/climateinfo'

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
        fecha_inicio = datetime.datetime.strptime(start, "%Y-%m-%d").date()
        fecha_fin = datetime.datetime.strptime(end, "%Y-%m-%d").date()
        longfiltertweets = mongo.db.longfiltertweets
        output = []
        for s in longfiltertweets.find({'created_at': {'$gte': 'Sat Sep 12 14:42:42 +0000 2020', '$lt':'Thu Sep 13 04:12:40 +0000 2020'}}):
          output.append({'id_str' : s['id_str'],'username' : s['username'],'created_at' : s['created_at'],'tweet' : s['tweet']})
        return jsonify({'longfiltertweets' : output})
        # return jsonify(mongo.db)
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
