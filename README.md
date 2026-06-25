# Парсер PEP

Консольный парсер документации Python и PEP, написанный на Python с использованием BeautifulSoup.

Проект позволяет получать данные с официальной документации Python, выводить результат в консоль, отображать его в виде таблицы или сохранять в CSV-файл.

## Возможности

Парсер поддерживает несколько режимов работы:

* `whats-new` — собирает ссылки на статьи раздела “What’s New in Python”, заголовки и информацию об авторах/редакторах.
* `latest-versions` — собирает список версий Python и их статусы.
* `download` — скачивает архив документации Python.
* `pep` — собирает статистику по статусам PEP, сравнивает статусы из общей таблицы со статусами на страницах конкретных PEP и выводит итоговое количество документов по каждому статусу.

## Технологии

* Python
* BeautifulSoup4
* lxml
* requests-cache
* tqdm
* PrettyTable
* pytest
* flake8

## Установка

Клонируйте репозиторий:

```bash
git clone https://github.com/YuliiaProshina/bs4_parser_pep.git
cd bs4_parser_pep
```

Создайте виртуальное окружение:

```bash
python -m venv venv
```

Активируйте виртуальное окружение.

```bash
source venv/Scripts/activate
```

Установите зависимости:

```bash
pip install -r requirements.txt
```

## Запуск

Перейдите в директорию `src`:

```bash
cd src
```

Запустите парсер, указав режим работы:

```bash
python main.py <режим>
```

Доступные режимы:

```bash
python main.py whats-new
python main.py latest-versions
python main.py download
python main.py pep
```

## Дополнительные параметры

Очистить кеш перед запуском:

```bash
python main.py pep -c
```

Вывести результат в виде таблицы:

```bash
python main.py pep -o pretty
```

Сохранить результат в CSV-файл:

```bash
python main.py pep -o file
```

## Результаты работы

При сохранении в файл результаты записываются в директорию:

```text
src/results/
```

Имя файла формируется автоматически и содержит режим работы парсера и дату запуска.

Пример:

```text
pep_2026-06-22_21-30-15.csv
```

## Пример вывода

Пример результата для режима `pep`:

```text
Статус    Количество
Active    35
Final     250
Draft     80
Всего     365
```

## Структура проекта

```text
bs4_parser_pep/
├── README.md
├── requirements.txt
├── src/
│   ├── main.py
│   ├── configs.py
│   ├── constants.py
│   ├── exceptions.py
│   ├── outputs.py
│   ├── utils.py
│   ├── results/
│   ├── downloads/
│   └── logs/
└── tests/
```

## Тесты

Запуск тестов:

```bash
pytest
```

Проверка стиля кода:

```bash
flake8 ./src
```

## Автор
Прошина Юлия - студент Яндекс.Практикума www.linkedin.com/in/yuliia-proshina-160551372
