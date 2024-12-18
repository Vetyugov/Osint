from urllib.parse import urlparse, urljoin

import colorama
from bs4 import BeautifulSoup

from web_utils import ParsedWebHtml

# запускаем модуль colorama
colorama.init()

GREEN = colorama.Fore.GREEN
GRAY = colorama.Fore.LIGHTBLACK_EX
RESET = colorama.Fore.RESET
YELLOW = colorama.Fore.YELLOW

# инициализировать set's для внутренних и внешних ссылок (уникальные ссылки)
internal_urls = set()
external_urls = set()

total_urls_visited = 0


def is_valid(url):
    """
    Проверка url
    """
    try:
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme)
    except (ValueError, TypeError):
        return False


def get_all_website_links(parsed_html: ParsedWebHtml, put_internal_links=True, put_external_links=False):
    """
    Возвращает все найденные URL-адреса на `url, того же веб-сайта.
    """
    # все URL-адреса `url`
    urls = set()
    # доменное имя URL без протокола
    domain_name = urlparse(parsed_html.url).netloc
    try:
        soup = BeautifulSoup(parsed_html.html, "html.parser")
        for a_tag in soup.findAll("a"):
            href = a_tag.attrs.get("href")
            if href == "" or href is None:
                # пустой тег href
                continue
            # присоединяемся к URL, если он относительный (не абсолютная ссылка)
            href = urljoin(parsed_html.url, href)
            parsed_href = urlparse(href)
            # удалить параметры URL GET, фрагменты URL и т. д.
            href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
            if not is_valid(href):
                # неверный URL
                continue
            if href in internal_urls:
                # уже в наборе
                continue
            if domain_name not in href:
                # внешняя ссылка
                if href not in external_urls:
                    print(f"{GRAY}[!] Внешняя ссылка: {href}{RESET}")
                    external_urls.add(href)
                continue
            print(f"{GREEN}[*] Внутреннея ссылка: {href}{RESET}")
            internal_urls.add(href)
    except (ConnectionError, OSError) as err:
        print(f'Не удалось загрузить список ссылок со страницы url = {url}', err)
    if put_internal_links:
        urls.update(internal_urls)
    if put_external_links:
        urls.update(external_urls)
    return urls


def crawl(url, max_urls=30):
    """
    Сканирует веб-страницу и извлекает все ссылки.
    Вы найдете все ссылки в глобальных переменных набора external_urls и internal_urls.
    параметры:
        max_urls (int): максимальное количество URL-адресов для сканирования, по умолчанию 30.
    """
    global total_urls_visited
    total_urls_visited += 1
    print(f"{YELLOW}[*] Проверено: {url}{RESET}")
    links = get_all_website_links(url)
    for link in links:
        if total_urls_visited > max_urls:
            break
        crawl(link, max_urls=max_urls)


# Тесты
if __name__ == "__main__":

    """
    parser = argparse.ArgumentParser(description="Link Extractor Tool with Python")
    parser.add_argument("url", help="The URL to extract links from.")
    parser.add_argument("-m", "--max-urls", help="Number of max URLs to crawl, default is 30.", default=30, type=int)

    args = parser.parse_args()
    url = args.url
    max_urls = args.max_urls
    """
    url = 'https://alumnus.susu.ru'
    max_urls = 500

    crawl(url, max_urls=max_urls)

    print("[+] Total Internal links:", len(internal_urls))
    print("[+] Total External links:", len(external_urls))
    print("[+] Total URLs:", len(external_urls) + len(internal_urls))
    print("[+] Total crawled URLs:", max_urls)

    domain_name = urlparse(url).netloc

    # сохранить внутренние ссылки в файле
    with open(f"{domain_name}_internal_links.txt", "w") as f:
        for internal_link in internal_urls:
            print(internal_link.strip(), file=f)

    # сохранить внешние ссылки в файле
    with open(f"{domain_name}_external_links.txt", "w") as f:
        for external_link in external_urls:
            print(external_link.strip(), file=f)
