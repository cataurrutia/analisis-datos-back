from pymongo import MongoClient
from nltk.corpus import stopwords
from googletrans import Translator
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

import pdmongo as pdm
import re
import pandas as pd
import nltk
import json
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import pymongo

MONGO_HOST = 'mongodb://localhost/twitterdb'


class TweetObject:
    # connection
    def connect_mongo(self):
        print("")
        print("Connecting to database and creating dataframe...")

        try:
            client = MongoClient(MONGO_HOST)

            db = client.climateinfo

            # Store info from "filtered_stream" collection into pandas dataframe
            df = pdm.read_mongo("filtered_stream", [], db)

            # print(df.head())
            return df

        except Exception as e:
            print(e)

    # Tweet manipulation: remove stopwords and 'rt', 'http', 'co', 'RT'
    def clean_tweets(self, df):
        print("")
        print("Manipulating [tweet], clean text...")

        # stop = nltk.download('stopwords')
        stopword_list = stopwords.words('spanish')

        # Create additional columns
        df['clean_tweets'] = None
        df['len'] = None

        # get rid of anything that isn't a letter
        for i in range(0, len(df['tweet'])):
            exclusion_list = ['[^a-zA-Z]', 'rt', 'http', 'co', 'RT']
            exclusions = '|'.join(exclusion_list)

            text = re.sub(exclusions, ' ', df['tweet'][i])
            text = text.lower()

            words = text.split()
            words = [word for word in words if not word in stopword_list]

            # Fill up columns with cleaned tweets and data length
            df.loc[:, 'clean_tweets'][i] = ' '.join(words)

        df.loc[:, 'len'] = np.array([len(tweet) for tweet in df['clean_tweets']])

        # print(df.head())
        return df

    # Tweet manipulation: format date -> "Tue Aug 11 22:37:25 +0000 2020" to "11-08-2020"
    def set_fecha(self, df):
        print("")
        print("Manipulating [created_at], creating [fecha]...")

        df['fecha'] = None
        valores_dias = []
        valores_meses = []
        valores_anos = []
        id_mes = []  # número del día en el mes

        # for each tweet use created_at to make formated "fecha_tweet" column
        for row in df['created_at']:
            ano = row[26:30]
            valores_anos.append(ano)

            numero = row[8:10]
            id_mes.append(numero)

            if re.search('Sun', row):
                valores_dias.append('Domingo')
            elif re.search('Mon', row):
                valores_dias.append('Lunes')
            elif re.search('Tue', row):
                valores_dias.append('Martes')
            elif re.search('Wed', row):
                valores_dias.append('Miercoles')
            elif re.search('Tue', row):
                valores_dias.append('Jueves')
            elif re.search('Fri', row):
                valores_dias.append('Viernes')
            elif re.search('Sat', row):
                valores_dias.append('Sabado')
            else:
                valores_dias.append('Otro/None')

            if re.search('Jan', row):
                valores_meses.append(1)
            elif re.search('Feb', row):
                valores_meses.append(2)
            elif re.search('Mar', row):
                valores_meses.append(3)
            elif re.search('Apr', row):
                valores_meses.append(4)
            elif re.search('May', row):
                valores_meses.append(5)
            elif re.search('Jun', row):
                valores_meses.append(6)
            elif re.search('Jul', row):
                valores_meses.append(7)
            elif re.search('Aug', row):
                valores_meses.append(8)
            elif re.search('Sep', row):
                valores_meses.append(9)
            elif re.search('Oct', row):
                valores_meses.append(10)
            elif re.search('Nov', row):
                valores_meses.append(11)
            elif re.search('Dec', row):
                valores_meses.append(12)
            else:
                valores_meses.append(0)

        #
        for i in range(len(valores_dias)):
            fecha = (id_mes[i] + '-' + str(valores_meses[i]) + '-' + valores_anos[i])

            # Fill up columns with cleaned tweets and data length
            df.loc[:, 'fecha'][i] = fecha

        # print(df.head())
        return df

    # Tweet manipulation: identify region for each tweet and add it to dataframe
    def add_region(self, df):
        print("")
        print("Manipulating [location], creating [region] and [id_region]...")

        nom_region = []
        id_region = []

        # dict con regiones
        regiones = {1: 'I Tarapacá', 2: 'II Antofagasta', 3: 'III Atacama', 4: 'IV Coquimbo', 5: 'V Valparaíso',
                    6: "VI O'Higgins", 7: 'VII Maule', 8: 'VIII Bíobío', 9: 'IX Araucanía', 10: 'X Los Lagos',
                    11: 'XI Aysén', 12: 'XII Magallanes', 13: 'RM Metropolitana', 14: 'XIV Los Ríos',
                    15: 'XV Arica y Parinacota', 16: 'XVI Ñuble', 17: 'No Especifíca'}

        # iteration for assignment of region to tweet
        for row in df['location']:
            if re.search('[Aa]rica', row) or re.search('[Pp]arina', row):
                nom_region.append(regiones[15])
                id_region.append(15)
            elif re.search('[Ii]quique', row) or re.search('[Tt]arap', row):
                nom_region.append(regiones[1])
                id_region.append(1)
            elif re.search('[Aa]ntof', row) or re.search('[Cc]ala', row) or re.search('[Tt]ocop', row) \
                    or re.search('[Ss]an Pe', row):
                nom_region.append(regiones[2])
                id_region.append(2)
            elif re.search('[Aa]taca', row) or re.search('[Cc]opia', row) or re.search('[Vv]allen', row):
                nom_region.append(regiones[3])
                id_region.append(3)
            elif re.search('[Ll]a [sS]er', row) or re.search('[Ss]erena', row) or re.search('[Cc]oquim', row):
                nom_region.append(regiones[4])
                id_region.append(4)
            elif re.search('[Vv]alpara', row) or re.search('[Pp]apudo', row) or re.search('[Vv]i[nñ]a', row) \
                    or re.search('[Vv]illa Ale', row) or re.search('[Qq]uil', row) or re.search('[Rr]e[ñn]ac', row) \
                    or re.search('[Cc]onc[óo]n', row):
                nom_region.append(regiones[5])
                id_region.append(5)
            elif re.search('[Ss]antiag', row) or re.search('[Qq]uinta [Nn]ormal', row) or re.search('[Mm]aipo', row) \
                    or re.search('[Mm]acul', row) or re.search('[Mm]elippilla', row) or re.search('[Rr]ecoleta', row) \
                    or re.search('[Rr]enca', row) or re.search('[Ll]o', row) or re.search('[Ss]an [Bb]ernard', row) \
                    or re.search('[sS]tgo', row) or re.search('[Pp]rovidencia', row) or re.search('[ÑñNn]u[ñn]oa', row) \
                    or re.search('[Ff]lorida', row) or re.search('[Pp]uente', row) or re.search('[Rr]eina', row) \
                    or re.search('[Bb]arnechea', row) or re.search('[Cc]ondes', row) or re.search('[Jj]oaqu[ií]n', row) \
                    or re.search('[Mm]aip[úu]', row) or re.search('[Vv]itacura', row) or re.search('[Pp]e[ñn]a', row) \
                    or re.search('[Ee]l [Bb]osque', row) or re.search('[Ll]a [Gg]ranja', row) \
                    or re.search('[Bb]u[íi]n', row) or re.search('[Mm]iguel', row):
                nom_region.append(regiones[13])
                id_region.append(13)
            elif re.search('[Rr]ancag', row) or re.search('[Rr]eng', row) or re.search('[Mm]achal', row) \
                    or re.search('[Pp]eum', row):
                nom_region.append(regiones[6])
                id_region.append(6)
            elif re.search('[Mm]aul', row) or re.search('[Cc]uric', row) or re.search('[Cc]auque', row) \
                    or re.search('[Ll]inar', row) or re.search('[Pp]arral', row) or re.search('[Tt]alca', row):
                nom_region.append(regiones[7])
                id_region.append(7)
            elif re.search('[ÑñNn]uble', row) or re.search('[Cc]hill', row) or re.search('[Yy]unga', row) \
                    or re.search('[Qq]uill[oó]n', row):
                nom_region.append(regiones[16])
                id_region.append(16)
            elif re.search('[Bb][íi]o', row) or re.search('[Cc]a[ñn]ete', row) or re.search('[Aa]rauc', row) \
                    or re.search('[Tt]ucape', row) or re.search('[Ll]os [AÁaá]ngeles', row) \
                    or re.search('[Tt]alcahuano', row) or re.search('[Cc]oncepci', row):
                nom_region.append(regiones[8])
                id_region.append(8)
            elif re.search('[Aa]raucan', row) or re.search('[Pp]uc[óo]n', row) or re.search('[Tt]emuco', row):
                nom_region.append(regiones[9])
                id_region.append(9)
            elif re.search('[Ll]os [rR][íi]os', row) or re.search('[Vv]aldivia', row) \
                    or re.search('[Ll]a [Uu]n[óo]n', row):
                nom_region.append(regiones[14])
                id_region.append(14)
            elif re.search('[Ll]os [Ll]agos', row) or re.search('[Cc]hilo[ée]', row) \
                    or re.search('[Pp]uerto [Mm]ontt', row) or re.search('[Cc]astro', row) \
                    or re.search('[Aa]ncud', row) or re.search('[Ff]rutillar', row) \
                    or re.search('[Pp]uerto [Vv]aras', row) or re.search('[Oo]sorno', row):
                nom_region.append(regiones[10])
                id_region.append(10)
            elif re.search('[Aa]ys[ée]n', row) or re.search('[Cc]oyhaique', row):
                nom_region.append(regiones[11])
                id_region.append(11)
            elif re.search('[Mm]agallanes', row) or re.search('[Pp]orvenir', row) \
                    or re.search('[Aa]nt[áa]rtica', row) or re.search('[Tt]ierra [Dd]el [fF]uego', row) \
                    or re.search('[Pp]unta [Aa]renas', row):
                nom_region.append(regiones[12])
                id_region.append(12)
            else:
                nom_region.append(regiones[17])
                id_region.append(17)

        # add lists to columns in dataframe
        df['region'] = nom_region
        df['id_region'] = id_region

        # print(df.head())
        return df

    # Tweet manipulation: sentiment analysis
    def sentiment(self, df):
        print("")
        print("Interpreting [tweet], creating [valoracion_manual]...")

        # - - - - Translate - - - -
        translator = Translator()
        valor = []

        # translate each tweet
        print("")
        print(".     . Translating tweets... ")

        for row in df['clean_tweets']:
            tr = translator.translate(str(row))
            valor.append(tr.text)
        df['traduccion'] = valor

        # - - - - Analyze valoracion (polaridad) - - - -
        analisis = SentimentIntensityAnalyzer()
        valoracion = {0: 'Neutro',
                      1: 'Positivo',
                      2: 'Negativo'}

        valores_id_sentimiento = []
        valores_manual = []

        print("")
        print(".     . Analizando polaridad de cada tweet... ")
        for row in df['traduccion']:
            res = analisis.polarity_scores(str(row))

            if res['compound'] >= 0.5:
                valores_manual.append(valoracion[1])
                valores_id_sentimiento.append(1)

            elif -0.5 < res['compound'] < 0.5:
                valores_manual.append(valoracion[0])
                valores_id_sentimiento.append(0)

            elif res['compound'] <= -0.5:
                valores_manual.append(valoracion[2])
                valores_id_sentimiento.append(2)

        df['valoracion_manual'] = valores_manual

        # print(df.head())
        # print(df.dtypes)
        return df

    # Tweet manipulation: agrupar por término más general
    def group_by_global(self, df):
        print("")
        print("Group by [grupo_clave]...")

        palabras_claves = {0: 'Biodiversidad', 1: 'Agua Potable', 2: 'Biodegradable', 3: 'Biofuel', 4: 'Biomasa',
                           5: 'Biorregionalismo', 6: 'Bosque', 7: 'Calentamiento Global', 8: 'Cambio Climático',
                           9: 'Capa de Ozono', 10: 'Comisión Nacional del Medio Ambiente', 11: 'Contaminación',
                           12: 'Contaminación Atmosférica', 13: 'Contaminación Biológica', 14: 'Deforestación',
                           15: 'Desarrollo Sostenible', 16: 'Desertización', 17: 'Deshielo', 18: 'Dióxido de Carbono',
                           19: 'Ecología', 20: 'Ecología Humana', 21: 'Ecosistema', 22: 'Ecotopía',
                           23: 'Educación ambiental', 24: 'Efecto Invernadero', 25: 'Energía Renovable',
                           26: 'Gestión Ambiental', 27: 'Glaciares', 28: 'Impacto Ambiental', 29: 'Industria',
                           30: 'Medio Ambiente', 31: 'Ministerio del Medio Ambiente', 32: 'Modernización Ecológica',
                           33: 'Problema Ambiental', 34: 'Monóxido de Carbono', 35: 'Fábricas', 36: 'Reciclaje',
                           37: 'Recursos Renovables', 38: 'Reloj Biológico', 39: 'Seguridad Alimentaria',
                           40: 'Sostenibilidad', 41: 'Tres R', 42: 'OTRO'}

        grupo = {0: 'Otro Grupo', 1: 'Bosques', 2: 'Cambio Climático', 3: 'Recursos Naturales', 4: 'Medio Ambiente',
                 5: 'Industrias', 6: 'Contaminación', 7: 'Biología', 8: 'Instituciones'}

        valores_claves = []
        valores_grupo = []
        valores_id = []

        # Assign each palabra_clave to a group (arbitrary)
        for row in df['tweet']:
            if re.search('[Aa]gua [Pp]otable', row):
                valores_claves.append(palabras_claves[1])
                valores_grupo.append(grupo[3])
                valores_id.append(3)
            elif re.search('[Bb]iodegrada', row):
                valores_claves.append(palabras_claves[2])
                valores_grupo.append(grupo[7])
                valores_id.append(7)
            elif re.search('[Bb]iodiversi', row):
                valores_claves.append(palabras_claves[0])
                valores_grupo.append(grupo[7])
                valores_id.append(7)
            elif re.search('[Bb]iofuel', row):
                valores_claves.append(palabras_claves[3])
                valores_grupo.append(grupo[7])
                valores_id.append(7)
            elif re.search('[Bb]iomasa', row):
                valores_claves.append(palabras_claves[4])
                valores_grupo.append(grupo[7])
                valores_id.append(7)
            elif re.search('[Bb]ioregionalis', row):
                valores_claves.append(palabras_claves[5])
                valores_grupo.append(grupo[7])
                valores_id.append(7)
            elif re.search('[Bb]osque', row):
                valores_claves.append(palabras_claves[6])
                valores_grupo.append(grupo[1])
                valores_id.append(1)
            elif re.search('[Cc]alentamiento [Gg]lobal', row):
                valores_claves.append(palabras_claves[7])
                valores_grupo.append(grupo[2])
                valores_id.append(2)
            elif re.search('[Cc]ambio [Cc]lim[áa]', row):
                valores_claves.append(palabras_claves[8])
                valores_grupo.append(grupo[2])
                valores_id.append(2)
            elif re.search('[Cc]apa [Oo]zono', row):
                valores_claves.append(palabras_claves[9])
                valores_grupo.append(grupo[4])
                valores_id.append(4)
            elif re.search('[Cc]omisi[óo]n [Mm]edio', row):
                valores_claves.append(palabras_claves[10])
                valores_grupo.append(grupo[8])
                valores_id.append(8)
            elif re.search('[Cc]ontaminaci [Aa]tmosf', row):
                valores_claves.append(palabras_claves[12])
                valores_grupo.append(grupo[6])
                valores_id.append(6)
            elif re.search('[Cc]ontaminaci [Bb]iol', row):
                valores_claves.append(palabras_claves[13])
                valores_grupo.append(grupo[6])
                valores_id.append(6)
            elif re.search('[Cc]ontaminaci', row):
                valores_claves.append(palabras_claves[11])
                valores_grupo.append(grupo[6])
                valores_id.append(6)
            elif re.search('[Dd]eforesta', row):
                valores_claves.append(palabras_claves[14])
                valores_grupo.append(grupo[1])
                valores_id.append(1)
            elif re.search('[Dd]esarrollo [Ss]osteni', row):
                valores_claves.append(palabras_claves[15])
                valores_grupo.append(grupo[8])
                valores_id.append(8)
            elif re.search('[Dd]esertizaci', row):
                valores_claves.append(palabras_claves[16])
                valores_grupo.append(grupo[4])
                valores_id.append(4)
            elif re.search('[Dd]eshielo', row):
                valores_claves.append(palabras_claves[17])
                valores_grupo.append(grupo[2])
                valores_id.append(2)
            elif re.search('[Dd]i[óo]xido', row):
                valores_claves.append(palabras_claves[18])
                valores_grupo.append(grupo[6])
                valores_id.append(6)
            elif re.search('[Ee]colog[íi]a [Hh]umana', row):
                valores_claves.append(palabras_claves[20])
                valores_grupo.append(grupo[3])
                valores_id.append(3)
            elif re.search('[Ee]colog', row):
                valores_claves.append(palabras_claves[19])
                valores_grupo.append(grupo[3])
                valores_id.append(3)
            elif re.search('[Ee]cosist', row):
                valores_claves.append(palabras_claves[21])
                valores_grupo.append(grupo[4])
                valores_id.append(4)
            elif re.search('[Ee]cotop[íi]a', row):
                valores_claves.append(palabras_claves[22])
                valores_id.append(4)
                valores_grupo.append(grupo[4])
            elif re.search('[Ee]ducaci[óo]n [Aa]mbiental', row):
                valores_claves.append(palabras_claves[23])
                valores_grupo.append(grupo[8])
                valores_id.append(8)
            elif re.search('[Ee]fecto [Ii]nvernad', row):
                valores_claves.append(palabras_claves[24])
                valores_grupo.append(grupo[2])
                valores_id.append(2)
            elif re.search('[Ee]nerg[íi]a [Rr]enovable', row):
                valores_claves.append(palabras_claves[25])
                valores_grupo.append(grupo[3])
                valores_id.append(3)
            elif re.search('[Gg]esti[óo]n [Aa]mbien', row):
                valores_claves.append(palabras_claves[26])
                valores_grupo.append(grupo[4])
                valores_id.append(4)
            elif re.search('[Gg]laciar', row):
                valores_claves.append(palabras_claves[27])
                valores_grupo.append(grupo[2])
                valores_id.append(2)
            elif re.search('[Ii]mpacto [Aa]mbienta', row):
                valores_claves.append(palabras_claves[28])
                valores_grupo.append(grupo[7])
                valores_id.append(7)
            elif re.search('[Ii]ndustria', row):
                valores_claves.append(palabras_claves[29])
                valores_grupo.append(grupo[5])
                valores_id.append(5)
            elif re.search('[Mm]edio [Aa]mbiente', row):
                valores_claves.append(palabras_claves[30])
                valores_grupo.append(grupo[4])
                valores_id.append(4)
            elif re.search('[Mm]inisterio [Mm]edio [Aa]mbiente', row):
                valores_claves.append(palabras_claves[31])
                valores_grupo.append(grupo[8])
                valores_id.append(8)
            elif re.search('[Mm]odernizaci[óo]n [Ee]col[óo]gica', row):
                valores_claves.append(palabras_claves[32])
                valores_grupo.append(grupo[8])
                valores_id.append(8)
            elif re.search('[Pp]roblema [Aa]mbiental', row):
                valores_claves.append(palabras_claves[33])
                valores_grupo.append(grupo[6])
                valores_id.append(6)
            elif re.search('[Mm]on[oó]xido', row):
                valores_claves.append(palabras_claves[34])
                valores_grupo.append(grupo[6])
                valores_id.append(6)
            elif re.search('[Ff[áa]brica', row):
                valores_claves.append(palabras_claves[35])
                valores_grupo.append(grupo[5])
                valores_id.append(5)
            elif re.search('[Rr]ecicla', row):
                valores_claves.append(palabras_claves[36])
                valores_grupo.append(grupo[3])
                valores_id.append(3)
            elif re.search('[Rr]ecursos [Rr]enovabl', row):
                valores_claves.append(palabras_claves[37])
                valores_grupo.append(grupo[3])
                valores_id.append(3)
            elif re.search('[Rr]eloj [Bb]iol[oó]gico', row):
                valores_claves.append(palabras_claves[38])
                valores_grupo.append(grupo[7])
                valores_id.append(7)
            elif re.search('[Ss]eguridad [Aa]liment', row):
                valores_claves.append(palabras_claves[39])
                valores_grupo.append(grupo[8])
                valores_id.append(8)
            elif re.search('[Ss]ostenibi', row):
                valores_claves.append(palabras_claves[40])
                valores_grupo.append(grupo[8])
                valores_id.append(8)
            elif re.search('[Tt3] [Rr][s]', row):
                valores_claves.append(palabras_claves[41])
                valores_grupo.append(grupo[8])
                valores_id.append(8)
            else:
                valores_claves.append(palabras_claves[42])
                valores_grupo.append(grupo[0])
                valores_id.append(0)

        df['grupo_clave'] = valores_grupo

        # print(df.head())
        # print(df.dtypes)
        return df

    # Save prepared data to csv
    def save_to_csv(self, df):
        try:
            df.to_csv(f'csv/prepared_data{dt.date.today()}.csv')
            print("\n")
            print("csv successfully saved, yaaaaaaaaay! \n")

        except Exception as e:
            print(e)

        return

    # Consolidate
    def save_to_collection(self, df):
        print("")
        print("Saving to prepared_tweets collection...")

        client = MongoClient(MONGO_HOST)
        db = client.climateinfo

        # actually saves "list" type, i know, wtf
        data_dict = df.to_dict('records')

        # iteramos en el df to save one by one and bypass the DuplicateKeyError
        for tweet in data_dict:
            try:
                db.prepared_tweets.insert_one(tweet)
                print('Saved to prepared_tweets collection')
                pass
            except pymongo.errors.DuplicateKeyError:
                continue

        return 'ok'


if __name__ == '__main__':
    t = TweetObject()

    data = TweetObject.connect_mongo(t)

    data = t.clean_tweets(data)
    data = t.set_fecha(data)
    data = t.add_region(data)
    data = t.sentiment(data)
    data = t.group_by_global(data)

    # t.save_to_csv(data)
    t.save_to_collection(data)
