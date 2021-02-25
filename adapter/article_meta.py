from xylose.scielodocument import Citation, Article


def to_doc_attrs(doc: Article):
    return {'pid': doc.publisher_id,
            'start_page': doc.start_page,
            'end_page': doc.end_page,
            'online_publication_date': doc.document_publication_date,
            'issue_publication_date': doc.issue_publication_date,
            'original_title': doc.original_title()}


def to_citref_attrs(cited_reference: Citation):
    pass
