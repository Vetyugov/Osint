# Для ожидания
from time import sleep

# Для отправки запросов
import requests
# Для работы с html
from bs4 import BeautifulSoup
# Для логирования действий
from loguru import logger
from selenium import webdriver

ATTEMPTS = 2  # Кол-во попыток получения ответа


class ParsedWebHtml:
    def __init__(self, url, html, text):
        self.url = url
        self.html = html
        self.text = text


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


def get_response_from(url):
    """Отправка запроса на сервер

    :param str url: Ссылка
    :return: Ответ сервера или None в виде строки
    """
    for i in range(ATTEMPTS):
        try:
            logger.debug(f"<GET {i} {url}>")
            r = requests.get(url, headers=None, timeout=20)
            if r.status_code == 200:
                logger.debug(f"<GET {i} {url}> - SUCCESSES")
                return r
        except Exception as e:
            logger.debug(f"<GET {i} failed {url}>, {e}")
            sleep(3)
    return None


def get_dynamic_html_from(url):
    print('init')
    driver = webdriver.Chrome()
    print('chrome created')
    driver.get(url)
    print('url send')

    results = driver.find_elements('//div[@class="yt-lockup-content"]')

    print(len(results))

    for result in results:
        video = result.find_element('.//h3/a')
        title = video.get_attribute('title')
        url = video.get_attribute('href')
        print("{} ({})".format(title, url))
    driver.quit()


def get_text_from_html(url, response: requests.Response):
    """
    Получить только текст из html
    :param html: вся страница htlm
    :return: только текстосодержащие поля
    """
    if response is not None and response.text is not None:
        soup = BeautifulSoup(response.text, 'html.parser')
        return ParsedWebHtml(url, response.text, soup.get_text())
    else:
        return None


def validate_link(url: str):
    return url.startswith('http')
