from xylose.scielodocument import Citation, Article


def _replace_none(data):
    return data if data else ''


def to_doc_attrs(doc: Article):
    attrs = {}

    keys_props = ['collection_acronym',
                  'publisher_id',
                  'start_page',
                  'end_page',
                  'document_publication_date',
                  'issue_publication_date',
                  'first_author']

    keys_funcs = ['original_title']

    for p in keys_props:
        attrs[p] = _replace_none(doc.__getattribute__(p))

    for f in keys_funcs:
        attrs[f] = _replace_none(doc.__getattribute__(f)())

    return attrs


def to_citref_attrs(cited_reference: Citation):
    pass
