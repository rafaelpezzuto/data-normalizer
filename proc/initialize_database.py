import argparse
import logging
import os
import sys
sys.path.append(os.getcwd())

from lib.database import create_tables


LOGGING_LEVEL = os.environ.get('LOGGING_LEVEL', 'INFO')
NORMALIZED_DATABASE_URI = os.environ.get('NORMALIZED_DATABASE_URI', 'mysql://127.0.0.1:3306/normalized')


def main():
    usage = 'Cria tabelas do banco de dados normalizados'
    parser = argparse.ArgumentParser(usage)

    parser.add_argument(
        '-u', '--norm_db_uri',
        default=NORMALIZED_DATABASE_URI,
        dest='norm_db_uri',
        help='String de conexão a base SQL no formato mysql://username:password@host1:port/database'
    )

    parser.add_argument(
        '--logging_level',
        choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'NOTSET'],
        dest='logging_level',
        default=LOGGING_LEVEL,
        help='Nível de log'
    )

    params = parser.parse_args()

    logging.basicConfig(level=params.logging_level)

    logging.info('Criando base de dados')
    create_tables(params.norm_db_uri)


if __name__ == '__main__':
    main()
