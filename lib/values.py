RAW_ARTICLE_META_CODE = 'am'
RAW_ISIS_CODE = 'isis'

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
