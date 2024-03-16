# Для отправки запросов
# Для ожидания
from time import sleep

import requests
# Для логирования действий
from loguru import logger

ATTEMPTS = 3  # Кол-во попыток получения ответа


def get_json_from(url):
    """Отправка запроса на сервер

    :param str url: Ссылка
    :return: Ответ сервера или None в виде json
    :rtype: dict | None
    """
    for i in range(ATTEMPTS):
        try:
            logger.debug(f"<GET {i} {url}")
            r = requests.get(url, headers=None, timeout=20)
            if r.status_code == 200:
                logger.debug(f"<GET {i} {url} - SUCCESSES")
                return r.json()
        except Exception as e:
            logger.debug(f"<GET {i} failed {url}, {e}")
            sleep(3)
    return None


def get_html_from(url):
    """Отправка запроса на сервер

    :param str url: Ссылка
    :return: Ответ сервера или None в виде строки
    :rtype: dict | None
    """
    for i in range(ATTEMPTS):
        try:
            logger.debug(f"<GET {i} {url}")
            r = requests.get(url, headers=None, timeout=20)
            if r.status_code == 200:
                logger.debug(f"<GET {i} {url} - SUCCESSES")
                return str(r.content)
        except Exception as e:
            logger.debug(f"<GET {i} failed {url}, {e}")
            sleep(3)
    return None
