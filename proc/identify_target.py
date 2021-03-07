import argparse
import logging
import os

from datetime import datetime, timedelta
from lib.database import mongo_collection
from model.target_identifier import TargetIdentifier

COLLECTION = os.environ.get('COLLECTION', 'bol')
LOGGING_LEVEL = os.environ.get('LOGGING_LEVEL', 'DEBUG')
NORMALIZED_DATABASE_URI = os.environ.get('NORMALIZED_DATABASE_URI', 'mysql://127.0.0.1:3306/normalized')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-f', '--from_date',
        default=(datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d'),
        help='Handle documents published from a date (YYYY-MM-DD)'
    )
    parser.add_argument(
        '-u', '--until_date',
        default=datetime.now().strftime('%Y-%m-%d'),
        help='Handle documents published until a date (YYYY-MM-DD)'
    )
    params = parser.parse_args()

    logging.basicConfig(level=params.logging_level,
                        format='[%(asctime)s] %(levelname)s %(message)s',
                        datefmt='%d/%b/%Y %H:%M:%S')

    tgi = TargetIdentifier()

    norm_db = mongo_collection(NORMALIZED_DATABASE_URI)
    documents_filter = {'$and': [{'collection': params.collection},
                                 {'processing_date': {'$gte': datetime.strptime(params.from_date, '%Y-%m-%d')}},
                                 {'processing_date': {'$lte': datetime.strptime(params.until_date, '%Y-%m-%d')}}]}

    for row in norm_db.find(documents_filter, no_cursor_timeout=True):
        pass


if __name__ == '__main__':
    main()
