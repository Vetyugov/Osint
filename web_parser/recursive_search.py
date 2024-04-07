from link_extractor import get_all_website_links
from web_utils import get_html_from
from crypto_address_parser.address_parser import CryptoAddressParser

links = [
    'https://stackoverflow.com/questions/71647566/blockchain-token-mint-error-nonce-too-low-address-0x1-f-current-nonce-491',
    # 'https://www.digitalocean.com/community/tutorials/python-str-repr-functions',
    'https://scam-alert.io/',
    'https://ru.investing.com/crypto/',
    'https://forklog.com/news',
    'https://forklog.com/'
]

searched_links = []
max_recursion_depth = 5
try_count = 0
results = []


def recursive_search(link, recursion_depth=0):
    crypto_address_parser = CryptoAddressParser()
    global try_count
    try_count += 1
    recursion_depth += 1
    if link in searched_links or recursion_depth >= max_recursion_depth:
        print(
            f'Достигнут предел глубины рекурсии {recursion_depth} из {max_recursion_depth} или ссылка уже анализировалась')
        return

    searched_links.append(link)

    html = get_html_from(link)
    if html is not None:
        found = crypto_address_parser.check_is_text_contains_crypto(html, source=link)
        if len(found) > 0:
            print(f'найден адрес {found}')
            for f in found:
                results.append(f)

    for sub_link in get_all_website_links(link):
        recursive_search(sub_link, recursion_depth)


if __name__ == '__main__':
    for main_link in links:
        recursive_search(main_link)

    print(f'Представлен результат анализа {try_count} страниц')
    print(results)
