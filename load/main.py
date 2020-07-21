import argparse
import logging
logging.basicConfig(level=logging.INFO)
import pandas as pd
from article import Article
from base import Base, engine, Session

logger = logging.getLogger(__name__)      #se declara el logger especifico que se utilizará para este archivo

def main(filename):
    Base.metadata.create_all(engine)   #para generar esquemas (schema)
    session = Session()                #se inicializa la sesion
    articles = pd.read_csv(filename)           #leer el csv

    for index, row  in  articles.iterrows():  #iterrows es una funcion de pandas que permite iterar por row
        logger.info('cargando la fila del articulo {}  dentro del DB'.format(row['uid']))
        article = Article(row['uid'],
                          row['body'],
                          row['host'],
                          row['newspaper_uid'],
                          row['tokens_body'],
                          row['tokens_title'],
                          row['title'],
                          row['url'])                #ojo, se debe tener cuidado con las rows, ya que deben estar en una posicion predefinida
        session.add(article) #esta función mete la iteración anterior dentro de la base de datos

    session.commit()          #sse debe iniciar la sesion
    session.close()           #se debe cerrar
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help= 'Importa tu archivo', type= str)
    args = parser.parse_args()
    main(args.filename)