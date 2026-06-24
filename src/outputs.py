import csv
import datetime as dt
import logging

from prettytable import PrettyTable

from constants import (DATETIME_FORMAT, FILE_OUTPUT, PRETTY_OUTPUT,
                       BASE_DIR, FILE_SAVED_MESSAGE)


def default_output(results, *args):
    for row in results:
        print(*row)


def pretty_output(results, *args):
    table = PrettyTable()
    table.field_names = results[0]
    table.align = 'l'
    table.add_rows(results[1:])
    print(table)


def file_output(results, cli_args):
    results_dir = BASE_DIR / 'results'
    results_dir.mkdir(exist_ok=True)
    parser_mode = cli_args.mode
    now_formatted = dt.datetime.now().strftime(DATETIME_FORMAT)
    file_name = f'{parser_mode}_{now_formatted}.csv'
    file_path = results_dir / file_name
    with open(file_path, 'w', encoding='utf-8') as f:
        writer = csv.writer(f, dialect=csv.unix_dialect)
        writer.writerows(results)
    logging.info(FILE_SAVED_MESSAGE.format(file_path=file_path))


OUTPUT_TO_FUNCTION = {
    PRETTY_OUTPUT: pretty_output,
    FILE_OUTPUT: file_output,
    None: default_output,
}


def control_output(results, cli_args):
    output_function = OUTPUT_TO_FUNCTION[cli_args.output]
    output_function(results, cli_args)
