import time
import logging
import pandas as pd

from link_extractor import get_all_website_links
from web_utils import get_static_html_from, validate_link, get_text_from_html
from crypto_address_parser.address_parser import CryptoAddressParser
from db_service import DataBaseService, WebParsedLink, WebFoundAddress
from datetime import datetime

# TODO: 1. Добавлять всю html в БД
# TODO: 2. На фронте добавить больше функционала
# TODO: 3. Написать docker.compose для автоматического развертывания приложения
# TODO: 4. Обрезать контекст по предложению
# TODO: 5. Научиться работать с динамическими сайтами (взять самый нужный один)
# TODO: 6. Сделать тг бота для поиска и алертинга

logging.basicConfig(level=logging.INFO, filename="metrics_log.log", filemode="w")
# Время врохода по каждой ссылке
# Двумерный массив(
#                   0 - получение html,
#                   1 - парсинг страницы,
#                   2 - сохранение в БД найденных адресов (опционально),
#                   3 - сохранение в БД проанализированную ссылку (опционально),
#                   4 - общее время)
metric_times = []
# Количество проходов по рекурсии в рамках одной mail_link
metric_recursion_counter = 0

MAX_RECURSION_DEPTH = 3
PARSE_URL_AS_STATIC_PAGES = True  # Иначе получить html как динамическую страницу
try_count = 0
results = []

db_service = DataBaseService()


def get_text_from_url(link):
    if 'https://www.youtube' in link:
        print(f'Ccылка {link} ведет на youtube - пропускаем')
        return None
    if PARSE_URL_AS_STATIC_PAGES:
        return get_text_from_html(get_static_html_from(link))
    else:
        print(f'ОШИБКА, установлен флаг PARSE_URL_AS_STATIC_PAGES = {PARSE_URL_AS_STATIC_PAGES}')


def recursive_search(link, from_link=None, recursion_depth=0):
    global metric_recursion_counter
    metric_recursion_counter += 1
    metric_start_time = time.time()
    metric_times_single = []

    crypto_address_parser = CryptoAddressParser()

    recursion_depth += 1
    if recursion_depth >= MAX_RECURSION_DEPTH:
        # print(f'Достигнут предел глубины рекурсии {recursion_depth} из {MAX_RECURSION_DEPTH}')
        return

    global try_count
    try_count += 1

    metric_read_html = time.time()
    parsed_html = get_text_from_url(link)
    metric_times_single.insert(0, (time.time() - metric_read_html))
    if parsed_html is not None:
        metric_parse = time.time()
        found = crypto_address_parser.check_is_text_contains_crypto(parsed_html.text, parsed_html.html, source=link)
        metric_times_single.insert(1, (time.time() - metric_parse))
        if len(found) > 0:
            print(f'найден адрес {found}')
            metric_save_db = time.time()
            for f in found:
                db_service.save_new_found_address(
                    WebFoundAddress(None, f.crypto_Name.name, f.pattern_Name, f.address, f.context, f.source,
                                    datetime.now(), f.valid_address))
                results.append(f)
            metric_times_single.insert(2, (time.time() - metric_save_db))
    metric_save_db_link = time.time()
    db_service.save_new_parsed_link(WebParsedLink(None, link, from_link, datetime.now()))
    metric_times_single.insert(3, (time.time() - metric_save_db_link))
    metric_times_single.insert(4, (time.time() - metric_start_time))
    metric_times.append(metric_times_single)

    for sub_link in get_all_website_links(link, put_external_links=True):
        # print(f'Попытка проанализировать ссылку: {link}')
        if validate_link(sub_link):
            print(f'Ссылка {sub_link} не валидна')
        elif db_service.is_link_already_parsed(sub_link):
            print(f'Ссылка {sub_link} уже анализировалась')
        else:
            recursive_search(sub_link, link, recursion_depth)


def save_metrics_to_csv(data):
    df = pd.DataFrame(data, columns=['html', 'parsing', 'address_db', 'link_db', 'total_time'])
    df.to_csv('metrics.csv', sep='\t')


if __name__ == '__main__':
    links = db_service.get_all_links_for_analize()
    print(f'ссылки для анализа {links}')
    logging.info(f"Для анализа взято ссылок {len(links)}")
    for main_link in links:
        metric_recursion_counter = 0
        logging.info(f"Начало обработки ссылки {main_link}")
        start = time.time()
        recursive_search(main_link.link)
        logging.info(f"{metric_recursion_counter} ссылок обработано за время {time.time() - start}")

    # logging.info(f"Метрики\n {metric_times}")

    db_service.close_connection()

    print(f'Представлен результат анализа {try_count} страниц')
    print(results)
    print('Сохраняем метрики...')
    save_metrics_to_csv(metric_times)
