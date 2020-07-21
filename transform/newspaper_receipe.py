import argparse               # para crear argumentos
import logging                    #lanza print, informacion en todo momento
logging.basicConfig(level=logging.INFO)
from urllib.parse import urlparse
import pandas as pd
import hashlib
import nltk
from nltk.corpus import stopwords

logger = logging.getLogger(__name__)

def main(filename):
    logger.info('comenzando el prroceso de limpieza')

    df = _read_data(filename)                                     #se leen los datos
    newspaper_uid = _extract_newspaper_uid(filename)               #se extrae el newspaper_uid
    df = _add_newspaper_uid_column(df,newspaper_uid)                #se agrega a la columna
    df = _extract_host(df)                                             #se extrae el host
    df = _fill_missing_titles(df)
    df = _generate_uids_for_rows(df)
    df = _remove_new_lines_from_body(df)
    df = _remove_duplicate_entries(df, 'title')
    df = tokenize_column(df, 'title')
    df = tokenize_column(df, 'body')
    df = _drop_rows_with_missing_values(df)
    df = _save_data(df, filename)


    return df

def _read_data(filename):                                           #con esta función se leen los datos
    logger.info('leyendo {}'.format(filename))
    return pd.read_csv(filename)                                       #se lee el archivo csv con el módulo pandas (clase#24)

def _extract_newspaper_uid(filename):                                   #funciona para extraer newspaper uid del dataframe
    logger.info('extrayendo newspaper id')
    newspaper_uid = filename.split('_')[0]                              #la funcion split separa las cadenas para pasarlas a listas, en este caso elige el primero 

    logger.info('Newspaper detectado en {}'.format(newspaper_uid))
    return newspaper_uid                                                #retorna el uid

def _add_newspaper_uid_column(df,newspaper_uid):
    logger.info('vamos a llenar la columna {} '.format(newspaper_uid))
    df['newspaper_uid'] = newspaper_uid

    return df                                           #se retorna la base de datos con newspaper_uid agregado

def _extract_host(df):
    logger.info('estamos extrayendo el host de las urls')
    df['host'] = df['url'].apply (lambda url: urlparse(url).netloc)     #funcion para agregar host a las filas
    return df

def _fill_missing_titles(df):                                            #funciónm reemplazar los None, de la tabla

    logger.info('filling missing titles')
    missing_titles_mask = df['title'].isna()                            #se inicializa la busqueda de los None

    missing_titles= (df[missing_titles_mask]['url']
                     .str.extract(r'(?P<missing_titles>[^/]+)$')
                     .applymap(lambda title: title.split('-'))
                     .applymap(lambda title_world_list: ' '.join(title_world_list))
                     )
    df.loc[missing_titles_mask, 'title'] = missing_titles.loc[:, 'missing_titles'] #se reemplaza los titulos que no están, por los que se agregaron anteriormente

    return df

def _generate_uids_for_rows(df):
    logger.info('Generadndo uids por cada row')
    uids = (df
            .apply(lambda row: hashlib.md5(bytes(row['url'].encode())), axis= 1)
            .apply(lambda hash_object: hash_object.hexdigest())
            )

    df ['uid'] = uids
    df.set_index('uid')

    return df
def _remove_new_lines_from_body(df):
    logger.info('Removiendo las \.n del body')

    stripped_body = (df
                     .apply(lambda row : row ['body'], axis=1)
                     .apply(lambda body: list(body))
                     .apply(lambda letters: list(map(lambda letter: letter.replace('\n', ''), letters)))
                     .apply(lambda letters: ''.join(letters))
                     )
    df['body'] = stripped_body

    return df

def tokenize_column(df, column_name):  # se declara la función para poder hacer el token con más de una columna, en este caso el titulo y el body
    stop_words = set(stopwords.words('spanish'))

    n_tokens = (df.dropna()  # se elimina si hay algo con None, porque si no la librería falla.
                .apply(lambda row: nltk.word_tokenize(row[column_name]),axis=1)  # separa las palabras que están dentro de la row
                .apply(lambda tokens: list(filter(lambda token: token.isalpha(),tokens)))  # elimina todas las palabras que no sean alfanumericas y se debe convertir en una lista
                .apply(lambda tokens: list(map(lambda token: token.lower(), tokens)))  # convertir todos los tokens en minusculas para poder compararlas posteriormente
                .apply(lambda word_list: list(filter(lambda word: word not in stop_words, word_list)))
                .apply(lambda valid_word_list: len(valid_word_list)))

    df['tokens_' + column_name] = n_tokens
    return df

def _remove_duplicate_entries(df, column_name):
    logger.info('Removing duplicate entries')
    df.drop_duplicates(subset=[column_name], keep='first', inplace=True)

    return df

def _drop_rows_with_missing_values(df):
    logger.info('Dropping rows with missing values')
    return df.dropna()

def _save_data(df, filename):
    clean_filename = 'clean_{}'.format(filename)
    logger.info('Saving data at location: {}'.format(clean_filename))
    df.to_csv(clean_filename)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument ('filename', help = 'The path the dirty data', type = str )
    arg = parser.parse_args()
    df = main(arg.filename)
    print(df)