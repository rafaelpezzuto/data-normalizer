import logging

from lib.string_processor import preprocess_default, preprocess_date
from model.cited_journal_normalizer import CitedJournalNormalizer


class Normalizer:
    def __init__(self, cjn: CitedJournalNormalizer):
        self.cjn = cjn

    def document(self, doc: dict):
        cl_title = preprocess_default(doc['original_title'])
        cl_first_author = preprocess_default(self.join_author(doc['first_author']))
        cl_publication_year = preprocess_date(doc['issue_publication_date'], return_int_year=True)
        cl_document_publication_date = preprocess_date(doc['document_publication_date'])
        cl_issue_publication_date = preprocess_date(doc['issue_publication_date'])

        doc.update({'cl_title': cl_title,
                    'cl_first_author': cl_first_author,
                    'cl_publication_year': cl_publication_year,
                    'cl_document_publication_date': cl_document_publication_date,
                    'cl_issue_publication_date': cl_issue_publication_date})

        return doc

    def cited_reference(self, cited_reference: dict):
        return cited_reference

    @staticmethod
    def join_author(author: dict):
        try:
            surname = author.get('surname', '')
            given_name = author.get('given_names', '')

            return ' '.join([given_name, surname]).strip()
        except AttributeError:
            logging.error('Campo author está vazio')
            return ''
