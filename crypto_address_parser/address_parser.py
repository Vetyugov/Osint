import enum
# для regex
import re

from bs4 import BeautifulSoup


class CryptoName(enum.Enum):
    """
    ENUM с перебором условных обозначений криптовалют
    """
    BTC = 0
    ETH = 1


class CheckCryptoResponse:
    """
    Класс-ответ, в котором описан результат сравнения слова с regex, в случае успешного match
    """

    def __init__(self, crypto_Name: CryptoName, pattern_Name: str, address: str, context: str = '', source: str = ''):
        self.crypto_Name = crypto_Name  # Сокращенное название криптовалюты
        self.pattern_Name = pattern_Name  # Название шаблона
        self.address = address  # Найденный адрес
        self.context = context  # Контекст в котором найден адрес
        self.source = source  # Источник

    def __str__(self):
        return f'{self.crypto_Name.name} - {self.pattern_Name} address = {self.address} sourse = {self.source} context = {self.context} \n'

    def __repr__(self):
        return f'{self.crypto_Name.name} - {self.pattern_Name} address = {self.address} sourse = {self.source} context = {self.context} \n'


# \W - Любой символ, кроме буквенного или цифрового символа или знака подчёркивания
# Паттерны для адресов Биткоина
BTC_ADDRESSES_REGEX_PATTERNS = {
    #В тексте
    'BTC Legacy address': re.compile(r'[^a-z0-9A-Z/]1[a-z0-9A-Z]{25,33}[^a-z0-9A-Z]', re.M | re.S),
    'BTC P2SH address': re.compile(r'[^a-z0-9A-Z/]3[a-z0-9A-Z]{25,33}[^a-z0-9A-Z]', re.M | re.S),
    'BTC Segwit address': re.compile(r'[^a-z0-9A-Z/]bc1[a-z0-9A-Z]{23,42}[^a-z0-9A-Z]', re.M | re.S),
    'BTC Taproot address': re.compile(r'[^a-z0-9A-Z/]bc1p[a-z0-9A-Z]{23,42}[^a-z0-9A-Z]', re.M | re.S),

    #Слово целиком
    'BTC Legacy address full': re.compile(r'^1[a-z0-9A-Z]{25,33}$', re.M | re.S),
    'BTC P2SH address full': re.compile(r'^3[a-z0-9A-Z]{25,33}$', re.M | re.S),
    'BTC Segwit address full': re.compile(r'^bc1[a-z0-9A-Z]{23,42}$', re.M | re.S),
    'BTC Taproot address full': re.compile(r'^bc1p[a-z0-9A-Z]{23,42}$', re.M | re.S)
}

# Паттерны для адресов Эфира
ETH_ADDRESSES_REGEX_PATTERNS = {
    # All Ethereum addresses have a length of 40 hexadecimal characters and begin with “0x”
    #В тексте
    'ETH address': re.compile(r'[^a-z0-9A-Z/]0x[0-9A-Fa-f]{40}[^a-z0-9A-Z]', re.M | re.S),

    #Слово целиком
    'ETH address full': re.compile(r'^0x[0-9A-Fa-f]{40}$', re.M | re.S)
}

# Словарь всех паттернов
PATTERNS = {
    CryptoName.BTC: BTC_ADDRESSES_REGEX_PATTERNS,
    CryptoName.ETH: ETH_ADDRESSES_REGEX_PATTERNS
}


# TODO: Дополнить списки


class CryptoAddressParser:

    def __init__(self, context_size: int = 500):
        """
        Парсер крипто адресов
        :param context_size: количество символов слева и справа от найденного слова, которые нужно взять в контекст
        """
        self.CONTEXT_SIZE = context_size

    def __check(self, pattern, word: str):
        """
        Проверяет, соответствует ли слово паттерну
        :param pattern: паттерн Pattern из библиотеки re
        :param word: слово, которое анализируем
        :return: результат true/false
        """
        is_match = re.match(pattern, word)
        return is_match

    def __checkIfTextHasPattern(self, pattern, text: str):
        """
        Находит в тексте все адреса подходящие под заданный паттерн
        :param pattern: паттерн Pattern из библиотеки re
        :param text: текст, который анализируем
        :return: список неповторяющихся совпадений
        """
        re_text = pattern.findall
        return set(re_text(text))

    def __get_context_from_text(self, text: str, target: str):
        """
        Находит контекст в text, в котором был найден target
        Если в тексте нет target - возвращает путую строку
        :param text: текст, в котором найден адрес
        :param target: слово, вокруг которого нужно взять контекст
        :return: контекст
        """
        text = re.sub(" +", " ", text)#Убираем лишние пробелы
        text = re.sub("\n+", "\n", text)  # Убираем лишние переносы строк
        start = text.index(target)
        if start == -1:
            return ""
        left = start - self.CONTEXT_SIZE
        if left < 0:
            left = 0
        right = start + len(target) + self.CONTEXT_SIZE
        if right > len(text):
            right = len(text)
        return text[left: right]


    def __get_web_context(self, text: str, target: str):
        """
        Находит в text тег HTML в котором указан target.
        :param text: текст, в котором осуществлять поиск
        :param target: искомое слово
        :return: Список всех тегов с содержимым на странице, где есть target
        Если в тексте не нашёлся target - возвращает пустой список
        """
        soup = BeautifulSoup(text, 'html.parser')
        footer_element = soup.find(text={target})
        return footer_element



    def __cat_not_address_symbols(self, address: str):
        """
        Обрезает крайний левый и крайний правый символы адреса, если они не являются числом или буквой
        :param address: адрес
        :return: обрезанный адрес
        """
        symbols = re.findall('\W', address)
        for s in symbols:
            address = address.replace(s, "")
        return address

    def check_is_word_any_crypto(self, word: str):
        """
        Проверяет, соответствует ли слово хотя бы одному известному шаблону
        :param word: проверяемое слово
        :return: результат проверки. None в случае не соотвтетсвия ни одному шаблону
        """
        found_list = []
        for crypto_name, pattern_dict in PATTERNS.items():
            for pattern_name, pattern in pattern_dict.items():
                if self.__check(pattern, word):
                    found_list.append(CheckCryptoResponse(crypto_name, pattern_name, self.__cat_not_address_symbols(word)))
        return found_list

    def check_is_text_contains_crypto(self, html: str, source: str = ''):
        """
        Проверяет содержится ли в тексте какой-либо известный крипто адрес
        :param html: html, в котором нужно осуществлять поиск
        :param source: источник, в котором был найден текст (ссылка на статью, ТГ канал и пр)
        :return: список найденных адресов (list of CheckCryptoResponse)
        """
        found_list_rs = []
        for crypto_name, pattern_dict in PATTERNS.items():
            for pattern_name, pattern in pattern_dict.items():
                found = self.__checkIfTextHasPattern(pattern, html)
                if len(found) != 0:
                    for f in found:
                        found_list_rs.append(
                            CheckCryptoResponse(
                                crypto_name,
                                pattern_name,
                                self.__cat_not_address_symbols(f),
                                self.__get_context_from_text(html, f),
                                source)
                        )
        return found_list_rs


# Ниже описаны примеры использования класса

if __name__ == '__main__':
    # Поиск криптоадресов в тексте

    # Пример одного найденного адреса в тексте (33yPjjSMGHPp8zj1ZXySNJzSUfVSbpXEuL)
    crypto_parser = CryptoAddressParser(context_size=10)
    list_of_results = crypto_parser.check_is_text_contains_crypto(
        text='ass="d-none d-sm-block d-md-none">33yPjjSMGHPp...zSUfVSbpXEuL</span><span class="d-sm-none">33yPj...pXEuL</span></span>\n<div><a href="https://blockstream.info/address/ 33yPjjSMGHPp8zj1ZXySNJzSUfVSbpXEuL" target="_blank" class="text-font-size-md text-font-size-sm" style="font-style: ',
        source='какая-то ссылка или источник'
    )
    print('Если в тексте 1 адрес = ' + str(list_of_results))

    # Пример двух найденного адреса в тексте (33yPjjSMGHPp8zj1ZXySNJzSUfVSbpXEuL и 3ABCD33yPjjSMGHPp8zj1ZXySfVSbpXEuL)
    crypto_parser = CryptoAddressParser(context_size=10)
    list_of_results = crypto_parser.check_is_text_contains_crypto(
        text='ass="d-none d-sm-block d-md-none">33yPjjSMGHPp...zSUfVSbpXEuL</span>3ABCD33yPjjSMGHPp8zj1ZXySfVSbpXEuL<span class="d-sm-none">33yPj...pXEuL</span></span>\n<div><a href="https://blockstream.info/address/ 33yPjjSMGHPp8zj1ZXySNJzSUfVSbpXEuL" target="_blank" class="text-font-size-md text-font-size-sm" style="font-style: ',
        source='какая-то ссылка или источник'
    )
    print('Если в тексте 2 адреса = ' + str(list_of_results))


    #отдельная проверка конкретного слова, является ли оно крипто адресом
    crypto_parser = CryptoAddressParser()
    #Позитивный кейс
    result = crypto_parser.check_is_word_any_crypto('33yPjjSMGHPp8zj1ZXySNJzSUfVSbpXEuL')
    print('Слово является крипто адресом = ' + str(result))
    #Неготивный кейс
    result = crypto_parser.check_is_word_any_crypto('asd3yPjjSMGHPp8zj1ZXySNJzSUfVSbpXEuL')
    print('Слово НЕ является крипто адресом = ' + str(result))
