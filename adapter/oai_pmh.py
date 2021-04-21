from datetime import datetime
from sickle import Sickle


from lib.values import RAW_OAI_PMH, RAW_OAI_PHM_HEADER_ATTRS, RAW_OAI_PMH_METADATA_ATTRS


def doc_raw_attrs(doc):
    attrs = {'gathering_source': RAW_OAI_PMH,
             'gathering_date': datetime.utcnow()}

    for k in RAW_OAI_PHM_HEADER_ATTRS:
        attrs[k] = getattr(doc.header, k)

    attrs['collection'] = 'pre'
    attrs['pid'] = getattr(doc.header, 'identifier')

    for k in RAW_OAI_PMH_METADATA_ATTRS:
        attrs[k] = doc.metadata.get(k, '')

    return attrs


URL_PREPRINTS_OAI = 'https://preprints.scielo.org/index.php/scielo/oai'


def list_records():
    sik = Sickle(URL_PREPRINTS_OAI, verify=False)
    records = sik.ListRecords(**{'metadataPrefix': 'oai_dc',
                                 'from': '2021-04-01',
                                 'until': '2021-04-07',
                                 'set': 'scielo'})
    for r in records:
        doc = doc_raw_attrs(r)
        print(doc)


if __name__ == '__main__':
    list_records()
