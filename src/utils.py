from bs4 import BeautifulSoup
from requests import RequestException

from exceptions import ParserFindTagException


PAGE_LOAD_ERROR_MESSAGE = (
    'Возникла ошибка при загрузке страницы {url}: {error}'
)
TAG_NOT_FOUND_MESSAGE = 'Не найден тег {tag} {attrs}'


def get_response(session, url, encoding='utf-8'):
    try:
        response = session.get(url)
        response.encoding = encoding
        return response
    except RequestException as error:
        raise ConnectionError(
            PAGE_LOAD_ERROR_MESSAGE.format(url=url, error=error)
        ) from error


def get_soup(session, url, encoding='utf-8', parser='lxml'):
    return BeautifulSoup(
        get_response(session, url, encoding=encoding).text,
        parser,
    )


def find_tag(soup, tag, attrs=None):
    attrs_for_search = {} if attrs is None else attrs
    searched_tag = soup.find(tag, attrs=attrs_for_search)
    if searched_tag is None:
        raise ParserFindTagException(
            TAG_NOT_FOUND_MESSAGE.format(tag=tag, attrs=attrs)
        )
    return searched_tag
