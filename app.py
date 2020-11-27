import datetime
import pdmongo as pdm
import pandas as pd
import re
import matplotlib.pyplot as plt
import numpy as np

from collections import Counter
from wordcloud import WordCloud, STOPWORDS
from flask import Flask, jsonify, render_template, url_for, request, redirect
from flask_pymongo import PyMongo
from pymongo import MongoClient
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
from wordcloud import WordCloud, STOPWORDS

app = Flask(__name__)

MONGO_HOST = 'mongodb://localhost:27017/climateinfo'
client = MongoClient(MONGO_HOST)
app.config["MONGO_URI"] = MONGO_HOST

db = client.climateinfo
mongo = PyMongo(app)


# on load
@app.route('/')
def hello_world():
    words = pd.read_csv('csv/search_terms_unique.csv')
    search_words = tuple(words['Tema'].to_list())
    print(type(search_words))

    grupo_clave = ('Otro Grupo', 'Bosques', 'Cambio Climático', 'Recursos Naturales', 'Medio Ambiente',
                   'Industrias', 'Contaminación', 'Biología', 'Instituciones')

    regiones = ('I Tarapacá', 'II Antofagasta', 'III Atacama', 'IV Coquimbo', 'V Valparaíso',
                "VI O'Higgins", 'VII Maule', 'VIII Bíobío', 'IX Araucanía', 'X Los Lagos',
                'XI Aysén', 'XII Magallanes', 'RM Metropolitana', 'XIV Los Ríos',
                'XV Arica y Parinacota', 'XVI Ñuble', 'No Especifíca')

    # return jsonify(search_words)
    return render_template('index.html', words=search_words, regiones=regiones, grupo_clave=grupo_clave)


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


# sumario valoración palabra
@app.route('/valoracion/')
def resumen_valoracion():
    palabra = request.args.get('palabra', type=str)

    df = pdm.read_mongo("prepared_tweets", [], db)
    # print(df.head())

    if palabra == 'todas':
        try:
            pos_tweets = [tweet for index, tweet in enumerate(df["clean_tweets"]) if
                          re.search('Positivo', df['valoracion_manual'][index])]
            neg_tweets = [tweet for index, tweet in enumerate(df["clean_tweets"]) if
                          re.search('Negativo', df['valoracion_manual'][index])]
            neu_tweets = [tweet for index, tweet in enumerate(df["clean_tweets"]) if
                          re.search('Neutro', df['valoracion_manual'][index])]

            valoraciones = {
                "palabra": palabra,
                "total_tweets": len(df['clean_tweets']),
                "can_pos": len(pos_tweets),
                "can_neg": len(neg_tweets),
                "can_neu": len(neu_tweets)
            }

            # print(valoraciones)
            return jsonify(valoraciones)

        except ValueError as e:
            pass
    else:
        try:
            pos_tweets = [tweet for index, tweet in enumerate(df["clean_tweets"]) if
                          re.search('Positivo', df['valoracion_manual'][index])]
            neg_tweets = [tweet for index, tweet in enumerate(df["clean_tweets"]) if
                          re.search('Negativo', df['valoracion_manual'][index])]
            neu_tweets = [tweet for index, tweet in enumerate(df["clean_tweets"]) if
                          re.search('Neutro', df['valoracion_manual'][index])]

            valoraciones = {
                "palabra": palabra,
                "total_tweets": len(df['clean_tweets']),
                "can_pos": 0,
                "can_neg": 0,
                "can_neu": 0
            }

            # print(valoraciones)
            return jsonify(valoraciones)

        except ValueError as e:
            pass


# palabra más repetida
@app.route('/palabra/')
def mas_repetida():
    palabra = request.args.get('palabra', type=str)
    df = pdm.read_mongo("prepared_tweets", [], db)

    if palabra == 'todas':
        try:
            result = Counter(" ".join(df["clean_tweets"]).split()).most_common(50)
            # print(result)

            result_df = pd.DataFrame(result, columns=['Palabra', 'Frequencia']).set_index('Palabra')
            print(result_df)
            result_df = result_df.to_json(orient='columns')

            return result_df

        except ValueError as e:
            pass
    else:
        try:
            return palabra

        except ValueError as e:
            pass


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
