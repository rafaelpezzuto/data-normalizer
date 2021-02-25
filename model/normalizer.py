from model.cited_journal_normalizer import CitedJournalNormalizer


class Normalizer:
    def __init__(self, cjn: CitedJournalNormalizer):
        self.cjn = cjn

    def document(self, doc: dict):
        pass

    def cited_reference(self, cited_reference: dict):
        pass
