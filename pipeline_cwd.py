import logging
logging.basicConfig(level=logging.INFO)
import subprocess  #lanza comandos en la terminal

logger = logging .getLogger(__name__)
news_sites_uids = ['eluniversal', 'elpais']  #variable que almacena que los nombres de las paginas a las cuales tamos haciendo el scraping

def main():
    _extract()
    _transform()
    _load()

def _extract():
    logger.info('comenzando el proceso de extración')
    for news_sites_uid in news_sites_uids:
        subprocess.run(['python', 'scraping.py', news_sites_uid], cwd='./extract')  #se ejecuta el scrapper por cada uno de los sitios de noticias #cwd = current working directory
        subprocess.run(['find', '.', '-name', '{}*'.format(news_sites_uid),
                       '-exec', 'mv', '{}', '../transform/{}_.csv'.format(news_sites_uid),';'], cwd='./extract')


def _transform():
    logger.info('comenzando la transformación')
    for news_sites_uid in news_sites_uids:
        dirty_data_filename= '{}_.csv'.format(news_sites_uid)  #archivo sucio
        clean_data_filename = 'clean_{}'.format(dirty_data_filename) #archivo limpio
        subprocess.run(['python', 'main.py',  dirty_data_filename], cwd='./transform')    #corre el script para limpiar el archivo sucio
        subprocess.run(['rm', dirty_data_filename], cwd= './tranform')     #borra el archivo sucio
        subprocess.run(['mv', clean_data_filename, '../load/{}.csv'.format(news_sites_uid)], cwd='./tranform')

def _load():
    logger.info('comenzando el proceso de carga')
    for news_sites_uid in news_sites_uids:
        clean_data_filename = 'clean_{}'.format(news_sites_uid)
        subprocess.run(['python', 'main.py', clean_data_filename], cwd='./load')
        subprocess.run(['rm', clean_data_filename], cwd='./load')



if __name__ == '__main__':
    main()