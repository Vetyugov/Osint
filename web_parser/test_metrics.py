import time

from crypto_address_parser import address_parser
from main import get_web_page

links = [
    'https://stackoverflow.com/questions/71647566/blockchain-token-mint-error-nonce-too-low-address-0x1-f-current-nonce-491',
    'https://www.digitalocean.com/community/tutorials/python-str-repr-functions',
    'https://scam-alert.io/']


def parse_by_word():
    for link in links:
        html = get_web_page(url=link)
        result = []
        sum_delta_time = 0
        count_times = 0
        word_count = 0
        if html is not None:
            word_list = html.split(" ")
            word_count += len(word_list)
            for word in word_list:
                t1 = time.time()
                response = address_parser.check_is_word_any_crypto(word)
                sum_delta_time += (time.time() - t1)
                count_times += 1
                if response is not None:
                    result.append(response)
        print(f'Исследовано слов = {word_count}, среднее время проверки слова = {sum_delta_time / count_times}')
        print(result)


def parse_by_text():
    for link in links:
        html = get_web_page(url=link)
        result = []
        if html is not None:
            t1 = time.time()
            response = address_parser.check_is_text_contains_crypto(html)
            result.append(response)
            print(f'Исследован текст длиной {len(html)} символов, время проверки текста = {time.time() - t1}')
        print(result)


if __name__ == '__main__':
    parse_by_word()
    parse_by_text()
