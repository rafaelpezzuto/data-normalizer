import logging
import pickle
import re


MIN_CHARS_LENGTH = 6
MIN_WORDS_COUNT = 2
STATUS_NOT_NORMALIZED = 0
STATUS_EXACT = 1
STATUS_EXACT_VALIDATED = 2
STATUS_EXACT_VALIDATED_LR = 3
STATUS_EXACT_VALIDATED_LR_ML1 = 4
STATUS_EXACT_VOLUME_INFERRED_VALIDATED = 5
STATUS_EXACT_VOLUME_INFERRED_VALIDATED_LR = 6
STATUS_EXACT_VOLUME_INFERRED_VALIDATED_LR_ML1 = 7
STATUS_FUZZY_VALIDATED = 8
STATUS_FUZZY_VALIDATED_LR = 9
STATUS_FUZZY_VALIDATED_LR_ML1 = 10
STATUS_FUZZY_VOLUME_INFERRED_VALIDATED = 11
STATUS_FUZZY_VOLUME_INFERRED_VALIDATED_LR = 12
STATUS_FUZZY_VOLUME_INFERRED_VALIDATED_LR_ML1 = 13
VOLUME_IS_ORIGINAL = 0
VOLUME_IS_INFERRED = 1
VOLUME_NOT_USED = -1


class CitedJournalNormalizer:
    def __init__(self, use_exact, use_fuzzy, cited_journal_data):
        self.use_exact = use_exact
        self.use_fuzzy = use_fuzzy

        try:
            with open(cited_journal_data, 'rb') as f:
                self.data = pickle.load(f)
        except FileNotFoundError:
            logging.error('File {0} does not exist'.format(cited_journal_data))
            exit(1)

    def extract_issnl_from_valid_match(self, valid_match: str):
        """
        Extrai ISSN-L a partir de uma chave ISSN-ANO-VOLUME.
        Caso o ISSN não exista no dicionário issn-to-issnl, considera o próprio ISSN como ISSN-L.

        :param valid_match: chave validada no formato ISSN-ANO-VOLUME
        :return: ISSN-L
        """
        if not valid_match:
            return ''

        els_valid_match = valid_match.split('-')
        if len(valid_match) == 3:
            issn, year, volume = els_valid_match
            issnl = self.data['issn-to-issnl'].get(issn, '')

            if not issnl:
                issnl = issn

            return issnl

        return ''

    def extract_issn_year_volume_keys(self, cited_year, cited_volume, issns: set):
        """
        Extrai chaves ISSN-YEAR-VOLUME para uma referência citada e lista de ISSNs.

        :param cited_year: ano do periódico citado
        :param cited_volume: volume do periódico citado
        :param issns: set de possíveis ISSNs
        :return: set de chaves ISSN-ANO-VOLUME
        """
        keys = set()

        if cited_year:
            if len(cited_year) > 4:
                cited_year = cited_year[:4]

            if len(cited_year) == 4 and cited_year.isdigit():
                if cited_volume and cited_volume.isdigit():
                    for i in issns:
                        keys.add('-'.join([i, cited_year, cited_volume]))
                    return keys, VOLUME_IS_ORIGINAL
                else:
                    for i in issns:
                        cit_vol_inferred = self.infer_volume(i, cited_year)
                        if cit_vol_inferred:
                            keys.add('-'.join([i, cited_year, cit_vol_inferred]))
                    return keys, VOLUME_IS_INFERRED

        return keys, VOLUME_NOT_USED

    def get_issns(self, matched_issnls: set):
        """
        Obtém todos os ISSNs associados a um set de ISSN-Ls.

        :param matched_issnls: ISSN-Ls casados para uma dada referência citada
        :return: set de ISSNs vinculados aos ISSNL-s
        """
        possible_issns = set()

        for mi in matched_issnls:
            possible_issns = possible_issns.union(
                set(
                    [j for j in self.data['issnl-to-data'].get(mi, {}).get('issns', [])]
                )
            )

        return possible_issns

    def get_journal_match_status(self, match_mode: str, mount_mode: int, db_used: str):
        """
        Obtém o status com base no modo de casamento, de volume utilizado e de base de validação utilizada.

        :param match_mode: modo de casamento ['exact', 'fuzzy']
        :param mount_mode: modo de obtenção da chave de validação ['VOLUME_IS_ORIGINAL', VOLUME_IS_INFERRED']
        :param db_used: base de validação utilizada ['lr', 'lr-ml1', 'default']
        :return: código de status conforme método utilizado
        """
        if mount_mode == VOLUME_IS_ORIGINAL:
            if match_mode == 'exact':
                if db_used == 'lr':
                    return STATUS_EXACT_VALIDATED_LR
                elif db_used == 'lr-ml1':
                    return STATUS_EXACT_VALIDATED_LR_ML1
                elif db_used == 'default':
                    return STATUS_EXACT_VALIDATED
            else:
                if db_used == 'lr':
                    return STATUS_FUZZY_VALIDATED_LR
                elif db_used == 'lr-ml1':
                    return STATUS_FUZZY_VALIDATED_LR_ML1
                elif db_used == 'default':
                    return STATUS_FUZZY_VALIDATED
        elif mount_mode == VOLUME_IS_INFERRED:
            if match_mode == 'exact':
                if db_used == 'lr':
                    return STATUS_EXACT_VOLUME_INFERRED_VALIDATED_LR
                elif db_used == 'lr-ml1':
                    return STATUS_EXACT_VOLUME_INFERRED_VALIDATED_LR_ML1
                elif db_used == 'default':
                    return STATUS_EXACT_VOLUME_INFERRED_VALIDATED
            else:
                if db_used == 'lr':
                    return STATUS_FUZZY_VOLUME_INFERRED_VALIDATED_LR
                elif db_used == 'lr-ml1':
                    return STATUS_FUZZY_VOLUME_INFERRED_VALIDATED_LR_ML1
                elif db_used == 'default':
                    return STATUS_FUZZY_VOLUME_INFERRED_VALIDATED

    def infer_volume(self, issn: str, year: str):
        """
        Infere o volume de um periódico a partir de issn-to-equation.

        :param issn: issn para o qual o volume será inferido
        :param year: ano do periódico citado
        :return: str do volume inferido arredondado para valor inteiro (se volume inferido for maior que 0)
        """
        equation = self.data['issn-to-equation'].get(issn)

        if equation:
            a, b, r2 = equation
            volume = a + (b * int(year))

            if volume > 0:
                return str(round(volume))

    def match_exact(self, journal_title: str):
        """
        Procura journal_title de forma exata no dicionário title-to-issnl.

        :param journal_title: título do periódico citado
        :return: set de ISSN-Ls associados de modo exato ao título do periódico citado
        """
        return self.data['title-to-issnl'].get(journal_title, set())

    def match_fuzzy(self, journal_title: str):
        """
        Procura journal_title de forma aproximada no dicionário title-to-issnl.

        :param journal_title: título do periódico citado
        :return: set de ISSN-Ls associados de modo aproximado ao título do periódico citado
        """
        matches = set()

        words = journal_title.split(' ')

        if len(journal_title) > MIN_CHARS_LENGTH and len(words) >= MIN_WORDS_COUNT:
            # O título oficial deve iniciar com a primeira palavra do título procurado
            pattern = r'[\w|\s]*'.join([word for word in words]) + '[\w|\s]*'
            title_pattern = re.compile(pattern, re.UNICODE)

            # O título oficial deve iniciar com a primeira palavra do título procurado
            for official_title in [ot for ot in self.data['title-to-issnl'].keys() if ot.startswith(words[0])]:
                if title_pattern.fullmatch(official_title):
                    matches = matches.union(self.data['title-to-issnl'][official_title])
        return matches

    def _mount_normalized_journal(self, status: int, key=None, issn_l=None):
        if not issn_l:
            issn_l = self.extract_issnl_from_valid_match(key)

        attrs = self.data['issnl-to-data'].get(issn_l, {})

        return {'issn-l': issn_l,
                'issn': attrs.get('issns', []),
                'official-journal-title': attrs.get('main-title', ''),
                'official-abbreviated-journal-title': attrs.get('main-abbrev-title', ''),
                'alternative-journal-titles': attrs.get('alternative-titles', ''),
                'status': status}

    def validate_match(self, keys, use_lr=False, use_lr_ml1=False):
        """
        Valida chaves ISSN-ANO-VOLUME nas bases de validação
        :param keys: chaves em formato ISSN-ANO-VOLUME
        :param use_lr: valida com dados de regressão linear de ISSN-ANO-VOLUME
        :param use_lr_ml1: valida com dados de regressão linear de ISSN-ANO-VOLUME mais ou menos 1
        :return: chaves validadas
        """
        valid_matches = set()

        if use_lr:
            validating_base = self.data['issn-year-volume-lr']
        elif use_lr_ml1:
            validating_base = self.data['issn-year-volume-lr-ml1']
        else:
            validating_base = self.data['issn-year-volume']

        for k in keys:
            if k in validating_base:
                valid_matches.add(k)

        return valid_matches

    def normalize_cited_journal(self, cited_year, cited_volume, cleaned_cit_journal_title, mode='exact'):
        if mode == 'fuzzy':
            matches = self.match_fuzzy(cleaned_cit_journal_title)
        else:
            matches = self.match_exact(cleaned_cit_journal_title)

        # Verifica se houve casamento com apenas com um ISSN-L e se é casamento exato
        if len(matches) == 1 and mode == 'exact':
            return self._mount_normalized_journal(status=STATUS_EXACT, issn_l=matches.pop())

        # Verifica se houve casamento com mais de um ISSN-L ou se é casamento aproximado e houve apenas um casamento
        elif len(matches) > 1 or (mode == 'fuzzy' and len(matches)) == 1:
            # Carrega todos os ISSNs possiveis associados aos ISSN-Ls casados
            possible_issns = self.get_issns(matches)

            if possible_issns:
                # Monta chaves ISSN-ANO-VOLUME
                keys, mount_mode = self.extract_issn_year_volume_keys(cited_year,
                                                                      cited_volume,
                                                                      possible_issns)

                if keys:
                    # Valida chaves na base de ano e volume
                    cit_valid_matches = self.validate_match(keys)

                    if len(cit_valid_matches) == 1:
                        status = self.get_journal_match_status(mode, mount_mode, 'default')
                        return self._mount_normalized_journal(status, cit_valid_matches.pop())

                    elif len(cit_valid_matches) == 0:
                        # Valida chaves na base de regressão linear
                        cit_valid_matches = self.validate_match(keys, use_lr=True)

                        if len(cit_valid_matches) == 1:
                            status = self.get_journal_match_status(mode, mount_mode, 'lr')
                            return self._mount_normalized_journal(status, cit_valid_matches.pop())

                        elif len(cit_valid_matches) == 0:
                            # Valida chaves na base de regressão linear com volume flexibilizado
                            cit_valid_matches = self.validate_match(keys, use_lr_ml1=True)

                            if len(cit_valid_matches) == 1:
                                status = self.get_journal_match_status(mode, mount_mode, 'lr-ml1')
                                return self._mount_normalized_journal(status, cit_valid_matches.pop())

        return self._mount_normalized_journal(status=STATUS_NOT_NORMALIZED)
