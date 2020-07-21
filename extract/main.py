import argparse
import logging
import news_page_objects as news
import re
import datetime     #se importa este modulo de fechas
import csv          #se importa csv para guardar la informacion
from requests.exceptions import HTTPError
from config_yaml import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def _news_scraper(news_site_uid):
    host = config()['news_sites'][news_site_uid]['url']
    logging.info('Comenzanco el scraping en: {}'.format(host))

    homepage = news.HomePage(news_site_uid, host)

    articles = []   #lista de articulos que se encontrarán

    for link in homepage.article_links:
        article = _fetch_article(news_site_uid, host, link)

        if article: #se ejecuta si es que hay un articulo
            logger.info('se encontro el articulo')
            articles.append(article)
            print('titulo = {}'.format(article.title))


    _save_articles(news_site_uid, articles)                 #se inicializa esta funcion que servirá de guardado

    print('cantidad de articulos es de : {}'.format(len(articles)))

def _save_articles(news_site_uid, articles):                #guardará en un archivo la informacion
    now = datetime.datetime.now().strftime('%Y_%m_%d')          #se inicializa el datetime, y se le da formato con string format time
    out_file_name = '{}_{}_articles.csv'.format(news_site_uid, now)
    csv_headers = list(filter(lambda property: not property.startswith('_'), dir(articles[0])))  #se filtra la informacion mediante la funcion filter de dir
    with open(out_file_name, mode= 'w+') as f:                          #se emplea codificacion de manipulacion de archivos
        writer = csv.writer(f)                                             #se inicializa un writer
        writer.writerow(csv_headers)                                     #se pide que escriba en la columna del archivo csv

        for article in articles:
            row = [str(getattr(article, prop))for prop in csv_headers] #row almacena los atributos de article y prop que se encuentran en csv_headers, getattr = es la forma de obtener atributos de una funcion
            writer.writerow(row)                                       #funcion para escribir el row en cada casilla en el archivo csv que retornará




def _fetch_article(news_site_uid, host, link):
    logger.info('esta buscando el archivo en {}'.format(link))
    article = None

    try:
        article = news.ArticlePage(news_site_uid, _build_link(host, link))
    except (HTTPError) as e:
        logger.warning('Error mientras se buscaba el articulo', exc_info= False)

    if article and not article.body:
        logger.warning('articulo invalido, no hay cuerpo en el articulo')
        return None

    return article


is_well_formed_link = re.compile(r'^https?://.+/.+$')
is_root_path = re.compile(r'^/.+$')

def _build_link(host, link):
    if is_well_formed_link.match(link):
        return link
    elif is_root_path.match(link):
        return '{}/{}'.format(host, link)
    else:
        return '{}/{}'.format(host, link)



if __name__ == '__main__':
    parser = argparse.ArgumentParser('siempre debe iniciar el parse así')
    news_site_choices = list(config()['news_sites'].keys())
    parser.add_argument('news_site',
                        help= 'Escoge el sitio el cual quieres buscar',
                        type= str,
                        choices= news_site_choices)

    arg = parser.parse_args()
    _news_scraper(arg.news_site)