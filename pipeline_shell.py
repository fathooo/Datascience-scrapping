# -*- coding: utf-8 -*-
import logging

logging.basicConfig(level=logging.INFO)
import subprocess  # para manipular directamente archivos de terminal
import datetime

logger = logging.getLogger(__name__)
news_sites_uids = ['eluniversal', 'elpais']

def main():
    _extract()
    _transform()
    _load()

def _extract():
    logger.info('Starting extract process')
    # now = datetime.datetime.now().strftime('%Y_%m_%d')
    for news_site_uid in news_sites_uids:
        subprocess.run(['python', 'main.py', news_site_uid],
                       cwd='./extract')  # ejecutamos nuestro web scraper por cada uno de nuestros sitios de noticias, #mover (mv) los archivos que se generaron. exec-ejecute algo por cada archivo que encuentre
        subprocess.run(['copy', r'C:\Users\felip\DataLifeProyecto\automatizacion_pipline\extract*.csv',
                        r'C:\Users\felip\DataLifeProyecto\automatizacion_pipline\transform'], shell=True)  # , cwd='./extract')

def _transform():
    logger.info('Starting transform process')
    now = datetime.datetime.now().strftime('%Y_%m_%d')
    for news_site_uid in news_sites_uids:
        dirty_data_filename = '{}_{datetime}_articles.csv'.format(news_site_uid, datetime=now)
        # clean_data_filename = 'clean_{}'.format(dirty_data_filename)
        subprocess.run(['python', 'main.py', dirty_data_filename],
                       cwd='./transform')  # ejecutamos nuestro programa de transform
        subprocess.run(['del', dirty_data_filename], shell=True, cwd='./transform')
        subprocess.run(['copy', r'C:\Users\felip\DataLifeProyecto\automatizacion_pipline\transform*.csv',
                        r'C:\Users\felip\DataLifeProyecto\automatizacion_pipline\load'
                        ], shell=True)  # cwd='./transform')

def _load():
    logger.info('Starting load process')
    now = datetime.datetime.now().strftime('%Y_%m_%d')
    for news_site_uid in news_sites_uids:
        clean_data_filename = 'clean_{}_{datetime}_articles.csv'.format(news_site_uid, datetime=now)
        subprocess.run(['python', 'main.py', clean_data_filename], cwd='./load')
        # subprocess.run(['del', 'clean_{}_{datetime}_articles.csv'.format(news_site_uid,datetime=now)], shell=True, cwd='./load')

if __name__ == '__main__':
    main()