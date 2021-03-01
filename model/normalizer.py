from xylose.scielodocument import Article, Citation, UnavailableMetadataException
from lib.string_processor import preprocess_default, preprocess_date
from lib.values import NORM_DOCUMENT_ATTRS, NORM_CITATION_ATTRS
from model.cited_journal_normalizer import CitedJournalNormalizer


class Normalizer:
    def __init__(self, cjn: CitedJournalNormalizer):
        self.cjn = cjn

    def document(self, data):
        norm_data = {}

        tmp_article = Article(data)

        for k, v in NORM_DOCUMENT_ATTRS.items():
            try:
                if v == 'publication_date':
                    norm_data[k] = preprocess_date(tmp_article.publication_date, return_int_year=True)
                elif v == 'original_title':
                    norm_data[k] = preprocess_default(tmp_article.original_title())
                else:
                    norm_data[k] = preprocess_default(getattr(tmp_article, v))
            except UnavailableMetadataException:
                pass
            except AttributeError:
                pass
            except TypeError:
                pass

        return norm_data

    def citations(self, data):
        norm_data = []

        if 'citations' in data:
            for d in data['citations']:
                tmp_citation = Citation(d)

                cit_data = {}
                for k, v in NORM_CITATION_ATTRS.items():
                    try:
                        if v == 'first_author':
                            cit_data[k] = preprocess_default(self.join_author(getattr(tmp_citation, v)))
                        elif v == 'publication_year':
                            cit_data[k] = preprocess_date(tmp_citation.publication_date, return_int_year=True)
                        elif v == 'index_number':
                            cit_data[k] = tmp_citation.index_number
                        else:
                            cit_data[k] = preprocess_default(getattr(tmp_citation, v))
                    except AttributeError:
                        pass
                    except TypeError:
                        pass
                norm_data.append(cit_data)

        return norm_data

    @staticmethod
    def join_author(author: dict):
        try:
            surname = author.get('surname', '')
            given_name = author.get('given_names', '')

            return ' '.join([given_name, surname]).strip()
        except AttributeError:
            return ''
