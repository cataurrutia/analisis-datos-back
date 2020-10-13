from pymongo import MongoClient
import pdmongo as pdm
import re

MONGO_HOST = 'mongodb://localhost/twitterdb'


class Limpieza:
    # connection
    def connect_mongo(self):
        try:
            client = MongoClient(MONGO_HOST)

            db = client.climateinfo

            # Store info from "filtered_stream" collection into pandas dataframe
            df = pdm.read_mongo("filtered_stream", [], db)

            print(df.head())
            return df

        except Exception as e:
            print(e)

    # Ubicación
    def location(self, df):
        serie_localizacion = []

        for tweet in df['location']:
            if re.search('[Cc]hile', tweet) or re.search('[Rr]egi[óo]n', tweet) or re.search('[Cc][Hh][Ll]', tweet):
                serie_localizacion.append('Chile')
            else:
                serie_localizacion.append('Otro')

        df['Localizacion'] = serie_localizacion
        df = df.loc[df.Localizacion == 'Chile']

        print(df.head())
        return df

    # Filtrar solo de Chile

    # Especificar region y/o comuna

    # Manejo de fecha


if __name__ == '__main__':
    l = Limpieza()

    data = Limpieza.connect_mongo(l)

    print(data)
