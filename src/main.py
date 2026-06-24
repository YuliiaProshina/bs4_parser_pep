import logging
import re
from collections import defaultdict
from urllib.parse import urljoin

import requests_cache
from requests import RequestException
from tqdm import tqdm

from configs import configure_argument_parser, configure_logging
from constants import (ALL_VERSIONS_NOT_FOUND_MESSAGE, ARCHIVE_SAVED_MESSAGE,
                       ARGS_MESSAGE, EXPECTED_STATUS,
                       MAIN_DOC_URL, PARSER_ERROR_MESSAGE,
                       PARSER_FINISHED_MESSAGE, PARSER_STARTED_MESSAGE,
                       PEP_URL, STATUS_MISMATCH_MESSAGE, BASE_DIR)
from exceptions import ParserFindTagException
from outputs import control_output
from utils import find_tag, get_response, get_soup


def whats_new(session):
    whats_new_url = urljoin(MAIN_DOC_URL, 'whatsnew/')
    soup = get_soup(session, whats_new_url)
    if soup is None:
        return
    sections_by_python = soup.select(
        '#what-s-new-in-python div.toctree-wrapper li.toctree-l1'
    )
    results = [('Ссылка на статью', 'Заголовок', 'Редактор, автор')]
    error_messages = []
    for section in tqdm(sections_by_python):
        version_a_tag = section.find('a')
        version_link = urljoin(whats_new_url, version_a_tag['href'])
        try:
            soup = get_soup(session, version_link)
        except RequestException as error:
            error_messages.append(str(error))
            continue
        results.append((
            version_link,
            find_tag(soup, 'h1').text,
            find_tag(soup, 'dl').text.replace('\n', ' '),
        ))
    for message in error_messages:
        logging.error(message)
    return results


def latest_versions(session):
    soup = get_soup(session, MAIN_DOC_URL)
    if soup is None:
        return
    sidebar = find_tag(soup, 'div', {'class': 'sphinxsidebarwrapper'})
    ul_tags = sidebar.find_all('ul')
    for ul in ul_tags:
        if 'All versions' in ul.text:
            a_tags = ul.find_all('a')
            break
    else:
        raise ParserFindTagException(ALL_VERSIONS_NOT_FOUND_MESSAGE)
    results = [('Ссылка на документацию', 'Версия', 'Статус')]
    pattern = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'
    for a_tag in a_tags:
        text_match = re.search(pattern, a_tag.text)
        if text_match is not None:
            version, status = text_match.groups()
        else:
            version, status = a_tag.text, ''
        results.append((a_tag['href'], version, status))
    return results


def download(session):
    downloads_url = urljoin(MAIN_DOC_URL, 'download.html')
    soup = get_soup(session, downloads_url)
    if soup is None:
        return
    pdf_a4_link = soup.select_one(
        'div[role="main"] table.docutils a[href$=".zip"]'
    )['href']
    archive_url = urljoin(downloads_url, pdf_a4_link)
    filename = archive_url.split('/')[-1]
    downloads_dir = BASE_DIR / 'downloads'
    downloads_dir.mkdir(exist_ok=True)
    archive_path = downloads_dir / filename
    response = get_response(session, archive_url)
    with open(archive_path, 'wb') as file:
        file.write(response.content)
    logging.info(ARCHIVE_SAVED_MESSAGE.format(archive_path=archive_path))


def pep(session):
    soup = get_soup(session, PEP_URL)
    if soup is None:
        return
    rows = soup.select('table.pep-zero-table tbody tr')
    status_counter = defaultdict(int)
    mismatch_messages = []
    for row in tqdm(rows):
        columns = row.find_all('td')
        information_tag = columns[0].find('abbr')
        if information_tag is None:
            continue
        status_tag = information_tag.text.strip()[1:]
        link_tag = row.find('a', {'class': 'pep reference internal'})
        pep_link = link_tag['href']
        pep_link_page = urljoin(PEP_URL, pep_link)
        pep_soup = get_soup(session, pep_link_page)
        if pep_soup is None:
            continue
        status_dt = None
        for dt_tag in pep_soup.find_all('dt'):
            if dt_tag.get_text(strip=True).startswith('Status'):
                status_dt = dt_tag
                break
        right_pep_status = status_dt.find_next_sibling('dd').get_text(
            strip=True)
        expected_statuses = EXPECTED_STATUS[status_tag]
        if right_pep_status not in expected_statuses:
            mismatch_messages.append(
                STATUS_MISMATCH_MESSAGE.format(
                    pep_link_page=pep_link_page,
                    right_pep_status=right_pep_status,
                    expected_statuses=expected_statuses,
                )
            )
        status_counter[right_pep_status] += 1
    for message in mismatch_messages:
        logging.info(message)
    return [
        ('Статус', 'Количество'),
        *status_counter.items(),
        ('Всего', sum(status_counter.values())),
    ]


MODE_TO_FUNCTION = {
    'whats-new': whats_new,
    'latest-versions': latest_versions,
    'download': download,
    'pep': pep,
}


def main():
    configure_logging()
    logging.info(PARSER_STARTED_MESSAGE)
    try:
        arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
        args = arg_parser.parse_args()
        logging.info(ARGS_MESSAGE.format(args=args))
        session = requests_cache.CachedSession()
        if args.clear_cache:
            session.cache.clear()
        parser_mode = args.mode
        results = MODE_TO_FUNCTION[parser_mode](session)
        if results is not None:
            control_output(results, args)
    except Exception:
        logging.exception(PARSER_ERROR_MESSAGE)
    logging.info(PARSER_FINISHED_MESSAGE)


if __name__ == '__main__':
    main()
