import html
import re
import unicodedata


parenthesis_pattern = re.compile(r'[-a-zA-ZÀ-ÖØ-öø-ÿ|0-9]*\([-a-zA-ZÀ-ÖØ-öø-ÿ|\W|0-9]*\)[-a-zA-ZÀ-ÖØ-öø-ÿ|0-9]*', re.UNICODE)
doi_pattern = re.compile(r'\d{2}\.\d+/.*$')
year_pattern = re.compile(r'\d{4}')
year_month_pattern = re.compile(r'\d{4}-\d{2}')
year_month_day_pattern = re.compile(r'\d{4}-\d{2}-\d{2}')

special_chars = ['@', '&']
special_words = ['IMPRESSO', 'PRINT', 'ONLINE', 'ELECTRONIC', 'CDROM']


def _remove_invalid_chars(text):
    vchars = []
    for t in text:
        if ord(t) == 11:
            vchars.append(' ')
        elif ord(t) >= 32 and ord(t) != 127:
            vchars.append(t)
    return ''.join(vchars)


def _remove_accents(text):
    return unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')


def _alpha_num_space(text, include_special_chars=False):
    new_str = []
    for character in text:
        if character.isalnum() or character.isspace() or (include_special_chars and character in special_chars):
            new_str.append(character)
        else:
            new_str.append(' ')
    return ''.join(new_str)


def _remove_double_spaces(text):
    while '  ' in text:
        text = text.replace('  ', ' ')
    return text.strip()


def preprocess_date(text, return_int_year=False):
    text = html.unescape(text)

    if return_int_year:
        matched_year = re.search(year_pattern, text)
        if matched_year:
            return matched_year.group()

    for p in [year_month_day_pattern, year_month_pattern]:
        matched_p = re.search(p, text)
        if matched_p:
            return matched_p.group()

    return text.lower()


def preprocess_default(text):
    text = html.unescape(text)
    text = _remove_accents(text)
    text = _alpha_num_space(text)
    text = _remove_double_spaces(text)
    return text.lower()


def preprocess_doi(text):
    doi = doi_pattern.findall(text)
    if len(doi) == 1:
        return doi[0].lower()


def preprocess_journal_title(text, use_remove_invalid_chars=False):
    text = html.unescape(text)

    if use_remove_invalid_chars:
        text = _remove_invalid_chars(text)

    parenthesis_search = re.search(parenthesis_pattern, text)
    while parenthesis_search is not None:
        text = text[:parenthesis_search.start()] + text[parenthesis_search.end():]
        parenthesis_search = re.search(parenthesis_pattern, text)

    for sw in special_words:
        text = text.replace(sw, '')
    return _remove_double_spaces(_alpha_num_space(_remove_accents(text), include_special_chars=True)).upper()
