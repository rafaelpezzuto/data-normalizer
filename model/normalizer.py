import logging

from lib.string_processor import preprocess_default, preprocess_date, preprocess_doi
from lib.values import ARTICLEMETA_DOCUMENT_CLEANED_FIELDS
from model.cited_journal_normalizer import CitedJournalNormalizer


class Normalizer:
    def __init__(self, cjn: CitedJournalNormalizer):
        self.cjn = cjn

    def document(self, doc: dict):
        cl_data = {}

        for d in doc.keys():
            if d in ARTICLEMETA_DOCUMENT_CLEANED_FIELDS:
                if d == 'original_title':
                    cl_data['cl_' + d] = preprocess_default(doc[d])

        doc.update(cl_data)

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
