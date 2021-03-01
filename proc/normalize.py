import argparse
import logging
import os
import sys
sys.path.append(os.getcwd())

from datetime import datetime, timedelta
from model.cited_journal_normalizer import CitedJournalNormalizer
from model.normalizer import Normalizer
from adapter.article_meta import doc_raw_attrs
from lib.database import mongo_collection, export_data


COLLECTION = os.environ.get('COLLECTION', 'bol')
LOGGING_LEVEL = os.environ.get('LOGGING_LEVEL', 'INFO')
CITED_JOURNAL_DATA = os.environ.get('CITED_JOURNAL_DATA', '/opt/data/bc-v1.bin')
MONGO_URI_ARTICLE_META = os.environ.get('MONGO_URI_ARTICLE_META', 'mongodb://127.0.0.1:27017/articlemeta.articles')
NORMALIZED_DATABASE_URI = os.environ.get('NORMALIZED_DATABASE_URI', 'mysql://127.0.0.1:3306/normalized')
NORMALIZED_DATABASE_PERSIST_BULK_SIZE = int(os.environ.get('NORMALIZED_DATABASE_PERSIST_BULK_SIZE', '100'))


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-j', '--cited_journal_data',
        default=CITED_JOURNAL_DATA
    )

    parser.add_argument(
        '-c', '--col',
        default=COLLECTION,
        dest='collection',
        help='Normalize a collection'
    )

    parser.add_argument(
        '-f', '--from_date',
        default=(datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d'),
        help='Normalize documents published from a date (YYYY-MM-DD)'
    )

    parser.add_argument(
        '-u', '--until_date',
        default=datetime.now().strftime('%Y-%m-%d'),
        help='Normalize documents published until a date (YYYY-MM-DD)'
    )

    parser.add_argument(
        '-x',
        '--use_exact_match',
        dest='use_exact',
        action='store_true',
        default=False,
        help='Use exact match to identify similar journals'
    )

    parser.add_argument(
        '-z',
        '--use_fuzzy_match',
        dest='use_fuzzy',
        action='store_true',
        default=False,
        help='Use fuzzy match to identifiy similar journals'
    )

    parser.add_argument(
        '-s',
        '--norm_db_uri',
        default=NORMALIZED_DATABASE_URI,
        help='Database normalized data string connection (mysql://user:pass@127.0.0.1:3306/database)'
    )

    parser.add_argument(
        '--logging_level',
        default=LOGGING_LEVEL
    )

    params = parser.parse_args()

    logging.basicConfig(level=params.logging_level,
                        format='[%(asctime)s] %(levelname)s %(message)s',
                        datefmt='%d/%b/%Y %H:%M:%S')

    logging.info('Criando normalizador de periódicos citados')
    cj_norm = CitedJournalNormalizer(use_exact=params.use_exact,
                                     use_fuzzy=params.use_fuzzy,
                                     cited_journal_data=params.cited_journal_data)

    logging.info('Criando normalizador de documentos e referências citadas')
    normalizer = Normalizer(cj_norm)

    article_meta = mongo_collection(MONGO_URI_ARTICLE_META)
    documents_filter = {'$and': [{'collection': params.collection},
                                 {'processing_date': {'$gte': datetime.strptime(params.from_date, '%Y-%m-%d')}},
                                 {'processing_date': {'$lte': datetime.strptime(params.until_date, '%Y-%m-%d')}}]}

    logging.info('Normalizando dados de coleção %s de %s a %s ' % (params.collection,
                                                                   params.from_date,
                                                                   params.until_date))

    data = []

    for doc in article_meta.find(documents_filter, no_cursor_timeout=True):
        logging.debug('Obtendo dados de %s...' % doc['code'])
        doc_attrs = doc_raw_attrs(doc)
        doc_attrs['norm_doc'] = normalizer.document(doc_attrs['data'])
        doc_attrs['norm_cits'] = normalizer.citations(doc_attrs['data'])
        data.append(doc_attrs)

        if len(data) >= NORMALIZED_DATABASE_PERSIST_BULK_SIZE:
            logging.info('Salvando raw data...')
            export_data(params.norm_db_uri, data)
            data = []

    logging.info('Salvando raw data...')
    export_data(params.norm_db_uri, data)


if __name__ == '__main__':
    main()
