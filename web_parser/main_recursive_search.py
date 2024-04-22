from link_extractor import get_all_website_links
from web_utils import get_html_from
from crypto_address_parser.address_parser import CryptoAddressParser
from db_service import DataBaseService, WebParsedLink, WebFoundAddress
from datetime import datetime

links = [
    # 'https://searchengines.guru/ru/forum/1038260',
    # 'https://tlap.com/forum/topic/21479-birzha-free2ex/'
    # 'https://stackoverflow.com/questions/71647566/blockchain-token-mint-error-nonce-too-low-address-0x1-f-current-nonce-491',
    # # 'https://www.digitalocean.com/community/tutorials/python-str-repr-functions',
    'https://scam-alert.io/',
    # 'https://ru.investing.com/crypto/',
    # 'https://forklog.com/news',
    # 'https://forklog.com/'
]

MAX_RECURSION_DEPTH = 3
try_count = 0
results = []

db_service = DataBaseService('osint_db.sqlite')

def recursive_search(link, from_link = None, recursion_depth=0):

    crypto_address_parser = CryptoAddressParser()

    recursion_depth += 1
    if recursion_depth >= MAX_RECURSION_DEPTH:
        print(f'Достигнут предел глубины рекурсии {recursion_depth} из {MAX_RECURSION_DEPTH}')
        return

    global try_count
    try_count += 1

    html = get_html_from(link)
    if html is not None:
        found = crypto_address_parser.check_is_text_contains_crypto(html, source=link)
        if len(found) > 0:
            print(f'найден адрес {found}')
            for f in found:
                db_service.save_new_found_address(WebFoundAddress(None, f.crypto_Name.name, f.pattern_Name, f.address, f.context, f.source, datetime.now()))
                results.append(f)
    db_service.save_new_parsed_link(WebParsedLink(None, link, from_link, datetime.now()))
    for sub_link in get_all_website_links(link, put_external_links=True):
        if db_service.is_link_already_parsed(sub_link):
            print(f'Ссылка {sub_link} уже анализировалась')
        else:
            recursive_search(sub_link, link, recursion_depth)




if __name__ == '__main__':
    for main_link in links:
        recursive_search(main_link)

    db_service.close_connection()

    print(f'Представлен результат анализа {try_count} страниц')
    print(results)

