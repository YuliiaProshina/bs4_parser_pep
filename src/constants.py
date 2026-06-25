from pathlib import Path

MAIN_DOC_URL = 'https://docs.python.org/3/'
PEP_URL = 'https://peps.python.org/'

DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'

EXPECTED_STATUS = {
    'A': ('Active', 'Accepted'),
    'D': ('Deferred',),
    'F': ('Final',),
    'P': ('Provisional',),
    'R': ('Rejected',),
    'S': ('Superseded',),
    'W': ('Withdrawn',),
    '': ('Draft', 'Active'),
}

PRETTY_OUTPUT = 'pretty'
FILE_OUTPUT = 'file'
OUTPUT_CHOICES = (PRETTY_OUTPUT, FILE_OUTPUT)

BASE_DIR = Path(__file__).parent
LOG_DIR = BASE_DIR / 'logs'
LOG_FILE = LOG_DIR / 'parser.log'

ARCHIVE_SAVED_MESSAGE = 'Архив был загружен и сохранён: {archive_path}'
PARSER_ERROR_MESSAGE = 'Во время работы парсера возникла ошибка.'
PARSER_STARTED_MESSAGE = 'Парсер запущен!'
PARSER_FINISHED_MESSAGE = 'Парсер завершил работу.'
ARGS_MESSAGE = 'Аргументы командной строки: {args}'
STATUS_MISMATCH_MESSAGE = (
    'Несовпадающие статусы: {pep_link_page}. '
    'Статус в карточке: {right_pep_status}. '
    'Ожидаемые статусы: {expected_statuses}'
)
ALL_VERSIONS_NOT_FOUND_MESSAGE = 'Не найден список All versions'
FILE_SAVED_MESSAGE = 'Файл с результатами был сохранён: {file_path}'
