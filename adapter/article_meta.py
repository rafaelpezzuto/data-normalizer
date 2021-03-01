import datetime

from lib.values import RAW_ARTICLE_META_ATTRS, RAW_ARTICLE_META_CODE


def doc_raw_attrs(doc):
    attrs = {'gathering_source': RAW_ARTICLE_META_CODE,
             'gathering_date': datetime.datetime.utcnow(),
             'collection': doc['collection'],
             'pid': doc['code']}

    data = {}
    for k in RAW_ARTICLE_META_ATTRS:
        data[k] = doc.get(k, '')
    attrs.update({'data': data})

    return attrs
