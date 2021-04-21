RAW_ARTICLE_META_CODE = 'am'
RAW_ISIS_CODE = 'isis'
RAW_OAI_PMH = 'oai'

RAW_ARTICLE_META_ATTRS = [
    # '_id',
    # 'applicable',
    'article',
    # 'body',
    'citations',
    # 'code',
    # 'code_title',
    # 'code_issue',
    # 'collection',
    # 'created_at',
    # 'doaj_id',
    'doi',
    'document_type',
    'fulltexts',
    'license',
    'processing_date',
    'publication_date',
    'publication_year',
    # 'sent_wos',
    'title',
    # 'validated_wos',
    # 'validated_scielo',
    # 'version'
]

RAW_OAI_PHM_HEADER_ATTRS = [
    'identifier',  # str
    # 'datestamp',  # str
    # 'setSpecs',  # list
]

RAW_OAI_PMH_METADATA_ATTRS = [
    'title',  # list
    'creator',  # list
    'subject'  # list
    'description',  # list
    'publisher',  # list
    'date',  # list
    'type',  # list
    'format',  # list
    'identifier',  # list
    'language',  # list
    'rights'  # list
]

NORM_DOCUMENT_ATTRS = {
    'issue': 'issue',
    'publication_type': 'document_type',
    'year': 'publication_date',
    'start_page': 'start_page',
    'title': 'original_title',
    'volume': 'volume'
}

NORM_CITATION_ATTRS = {
    'first_author': 'first_author',
    'issue': 'issue',
    'publication_type': 'publication_type',
    'year': 'publication_year',
    'start_page': 'start_page',
    'title': 'title',
    'volume': 'volume',
    'number': 'index_number'
}
