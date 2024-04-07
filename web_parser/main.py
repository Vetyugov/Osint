from crypto_address_parser import address_parser
import web_utils

links = [
    'https://stackoverflow.com/questions/71647566/blockchain-token-mint-error-nonce-too-low-address-0x1-f-current-nonce-491',
    'https://www.digitalocean.com/community/tutorials/python-str-repr-functions',
    'https://scam-alert.io/']


def get_web_page(url):
    print(f'Tring to get page with ulr = {url} ...')
    return web_utils.get_html_from(url)


def parser_html_and_find_address(html: str):
    """
    :param html: str with words
    :return: list of CheckCryptoResponse
    """
    result = []
    if html is not None :
        word_list = html.split(" ")
        for word in word_list:
            response = address_parser.check_is_word_any_crypto(word)
            if response is not None:
                result.append(response)
    return result


if __name__ == '__main__':
    result_for_task = {}
    for link in links:
        html = get_web_page(url=link)
        result_for_link = parser_html_and_find_address(html)
        if len(result_for_link) > 0:
            result_for_task[link] = result_for_link
    print(f'Удалось найти адреса: {result_for_task}')
