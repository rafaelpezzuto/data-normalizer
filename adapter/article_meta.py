import logging

from xylose.scielodocument import Citation, Article

from lib.values import (
    ARTICLEMETA_DOCUMENT_STR_FIELDS,
    ARTICLEMETA_DOCUMENT_METHOD_FIELDS
)


def _replace_none(data):
    return str(data) if data else ''


def to_doc_attrs(doc: Article):
    attrs = {}

    for p in ARTICLEMETA_DOCUMENT_STR_FIELDS:
        try:
            attrs[p] = _replace_none(doc.__getattribute__(p))
        except:
            logging.error('Problema para obter %s' % p)

    for f in ARTICLEMETA_DOCUMENT_METHOD_FIELDS:
        try:
            attrs[f] = _replace_none(doc.__getattribute__(f)())
        except:
            logging.error('Problema para obter %s()' % f)

    return attrs


def to_citref_attrs(cited_reference: Citation):
    pass
