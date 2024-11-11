import logging

import time
from datetime import datetime

from crypto_address_parser.address_parser import CryptoAddressParser
from db_service import DataBaseService, WebParsedLink, WebFoundAddress
from link_extractor import get_all_website_links
from metrics import WebOsintMetric, save_metrics_to_csv
from web_utils import get_response_from, validate_link, get_text_from_html

# TODO: 1. Добавлять всю html в БД
# TODO: 2. На фронте добавить больше функционала
# TODO: 3. Написать docker.compose для автоматического развертывания приложения
# TODO: 4. Обрезать контекст по предложению
# TODO: 5. Научиться работать с динамическими сайтами (взять самый нужный один)
# TODO: 6. Сделать тг бота для поиска и алертинга

FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO, filename="metrics_log.log", filemode="w")

# Количество проходов по рекурсии в рамках одной mail_link
metric_recursion_counter = 0

MAX_RECURSION_DEPTH = 200
PARSE_URL_AS_STATIC_PAGES = True  # Иначе получить html как динамическую страницу
SEARCH_EXTERNAL_LINKS = False

try_count = 0
results = []

current_metrics_list=[]

db_service = DataBaseService()
crypto_address_parser = CryptoAddressParser()


def get_parsed_web_html_from_url(link):
    if 'https://www.youtube' in link:
        print(f'Ccылка {link} ведет на youtube - пропускаем')
        return None
    if link.endswith('.pdf') or link.endswith('.xlsx') or link.endswith('.xls') or link.endswith(
            '.doc') or link.endswith('download'):
        print(f'Необходим обработчик для ФАЙЛА: {link}')
        with open('documents.txt', 'a', encoding='utf-8') as file:  # 'utf-8' кодировка помогает поддерживать различные символы
            file.write(f'Необходим обработчик для ФАЙЛА: {link}')  # Добавление текста
        return None
    if PARSE_URL_AS_STATIC_PAGES:
        return get_text_from_html(link, get_response_from(link))
    else:
        print(f'ОШИБКА, установлен флаг PARSE_URL_AS_STATIC_PAGES = {PARSE_URL_AS_STATIC_PAGES}')


def recursive_search(link, from_link=None, recursion_depth=0):
    try:

        start = time.time()
        global metric_recursion_counter
        metric_recursion_counter += 1

        recursion_depth += 1
        if recursion_depth >= MAX_RECURSION_DEPTH:
            print(f'Достигнут предел глубины рекурсии {recursion_depth} из {MAX_RECURSION_DEPTH}')
            return

        global try_count
        try_count += 1

        global current_metrics_list

        if metric_recursion_counter % 10 == 0:
            logging.info(f"Ссылок обработано: {metric_recursion_counter}")
            save_metrics_to_csv(metrics=current_metrics_list)
            current_metrics_list = []

        get_text_from_url_start = time.time()
        parsed_html = get_parsed_web_html_from_url(link)
        get_text_from_url_delta = time.time() - get_text_from_url_start

        check_is_text_contains_crypto_delta = 0
        save_new_found_address_delta = 0

        if parsed_html is not None:

            check_is_text_contains_crypto_start = time.time()
            found = crypto_address_parser.check_is_text_contains_crypto(parsed_html.text, parsed_html.html, source=link)
            check_is_text_contains_crypto_delta = time.time() - check_is_text_contains_crypto_start

            if len(found) > 0:
                print(f'найден адрес {found}')
                for f in found:
                    save_new_found_address_start = time.time()
                    db_service.save_new_found_address(
                        WebFoundAddress(None, f.crypto_Name.name, f.pattern_Name, f.address, f.context, f.source,
                                        datetime.now(), f.valid_address))
                    save_new_found_address_delta = time.time() - save_new_found_address_start
                    results.append(f)

            save_new_parsed_link_start = time.time()
            db_service.save_new_parsed_link(WebParsedLink(None, link, from_link, datetime.now()))
            save_new_parsed_link_delta = time.time() - save_new_parsed_link_start

            get_not_parsed_links_start = time.time()
            to_analize_list_of_links = db_service.get_not_parsed_links(
                get_all_website_links(parsed_html, put_external_links=SEARCH_EXTERNAL_LINKS))
            get_not_parsed_links_delta = time.time() - get_not_parsed_links_start

            total_time = time.time() - start
            metric = WebOsintMetric(
                link=link,
                total_time=total_time,
                get_text_from_url=get_text_from_url_delta,
                check_is_text_contains_crypto=check_is_text_contains_crypto_delta,
                save_new_found_address=save_new_found_address_delta,
                save_new_parsed_link=save_new_parsed_link_delta,
                get_not_parsed_links=get_not_parsed_links_delta
            )
            current_metrics_list.append(metric)

            for sub_link in to_analize_list_of_links:
                # print(f'Попытка проанализировать ссылку: {link}')
                if not validate_link(sub_link):
                    print(f'Ссылка {sub_link} не валидна')
                else:
                    recursive_search(sub_link, from_link, recursion_depth)
    except Exception as e:
        print(f'Произошла ошибка: {e.with_traceback()}')


if __name__ == '__main__':
    links = db_service.get_all_links_for_analize()
    print(f'ссылки для анализа {links}')
    logging.info(f"Для анализа взято {len(links)} ресурсов: {links}")
    for main_link in links:
        metric_recursion_counter = 0
        logging.info(f"Начало обработки ссылки {main_link}")
        start = time.time()
        recursive_search(main_link.link)
        logging.info(f"{metric_recursion_counter} ссылок обработано за время {time.time() - start} сек")

    db_service.close_connection()

    print(f'Представлен результат анализа {try_count} страниц')
    print(results)
    print('Сохраняем метрики...')
    # save_metrics_to_csv(metric_times)
