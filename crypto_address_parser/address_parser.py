import enum
import logging
# для regex
import re

from bs4 import BeautifulSoup


class CryptoName(enum.Enum):
    """
    ENUM с перебором условных обозначений криптовалют
    """
    BTC = 0
    ETH = 1
    DASH = 2
    XMR = 3
    ADA = 4
    ATOM = 5
    DOGE = 6
    MIOTA = 7
    LSK = 8
    LTC = 9
    XEM = 10
    NEO = 11
    ONT = 12
    DOT = 13
    XRP = 14
    XLM = 15
    TRC_20 = 16
    TRX = 17
    UNIVERSAL = 18


class CheckCryptoResponse:
    """
    Класс-ответ, в котором описан результат сравнения слова с regex, в случае успешного match
    """

    def __init__(self, crypto_Name: CryptoName, pattern_Name: str, address: str, context: str = '', source: str = '',
                 valid_address: bool = False):
        self.crypto_Name = crypto_Name  # Сокращенное название криптовалюты
        self.pattern_Name = pattern_Name  # Название шаблона
        self.address = address  # Найденный адрес
        self.context = context  # Контекст в котором найден адрес
        self.source = source  # Источник
        self.valid_address = valid_address  # Пройдена проверка валидности адреса

    def __str__(self):
        return f'{self.crypto_Name.name} - {self.pattern_Name} address = {self.address} sourse = {self.source} context = {self.context} \n'

    def __repr__(self):
        return f'{self.crypto_Name.name} - {self.pattern_Name} address = {self.address} sourse = {self.source} context = {self.context} \n'


# всё паттерны взяты с сайта https://gist.github.com/MBrassey/623f7b8d02766fa2d826bf9eca3fe005
# \W - Любой символ, кроме буквенного или цифрового символа или знака подчёркивания
# Паттерны для адресов Биткоина
BTC_ADDRESSES_REGEX_PATTERNS = {
    # В тексте
    'BTC Legacy address': re.compile(r'[^a-z0-9A-Z/]1[a-z0-9A-Z]{25,33}[^a-z0-9A-Z]', re.M | re.S),
    'BTC P2SH address': re.compile(r'[^a-z0-9A-Z/]3[a-z0-9A-Z]{25,33}[^a-z0-9A-Z]', re.M | re.S),
    'BTC Segwit address': re.compile(r'[^a-z0-9A-Z/]bc1[a-z0-9A-Z]{23,42}[^a-z0-9A-Z]', re.M | re.S),
    'BTC Taproot address': re.compile(r'[^a-z0-9A-Z/]bc1p[a-z0-9A-Z]{23,42}[^a-z0-9A-Z]', re.M | re.S),

    # Слово целиком
    'BTC Legacy address full': re.compile(r'^1[a-z0-9A-Z]{25,33}$', re.M | re.S),
    'BTC P2SH address full': re.compile(r'^3[a-z0-9A-Z]{25,33}$', re.M | re.S),
    'BTC Segwit address full': re.compile(r'^bc1[a-z0-9A-Z]{23,42}$', re.M | re.S),
    'BTC Taproot address full': re.compile(r'^bc1p[a-z0-9A-Z]{23,42}$', re.M | re.S)
}

# Паттерны для адресов Эфира
ETH_ADDRESSES_REGEX_PATTERNS = {
    # All Ethereum addresses have a length of 40 hexadecimal characters and begin with “0x”
    # В тексте
    'ETH address': re.compile(r'[^a-z0-9A-Z/]0x[0-9A-Fa-f]{40}[^a-z0-9A-Z]', re.M | re.S),

    # Слово целиком
    'ETH address full': re.compile(r'^0x[0-9A-Fa-f]{40}$', re.M | re.S)
}

DASH_ADDRESSES_REGEX_PATTERNS = {
    # В тексте
    'DASH address': re.compile(r'[^a-z0-9A-Z/]/X[1-9A-HJ-NP-Za-km-z]{33}[^a-z0-9A-Z]', re.M | re.S),

    # Слово целиком
    'DASH address full': re.compile(r'/X[1-9A-HJ-NP-Za-km-z]{33}$', re.M | re.S)
}

# Monero (XMR)
XMR_ADDRESSES_REGEX_PATTERNS = {
    # В тексте
    'XMR address': re.compile(r'[^a-z0-9A-Z/]/4[0-9AB][1-9A-HJ-NP-Za-km-z]{93}[^a-z0-9A-Z]', re.M | re.S),

    # Слово целиком
    'XMR address full': re.compile(r'/4[0-9AB][1-9A-HJ-NP-Za-km-z]{93}$', re.M | re.S)

}

# Далее паттерны взяты с ресурса https://publication.osintambition.org/20-regular-expressions-examples-to-search-for-data-related-to-cryptocurrencies-43e31dd4a5dc?gi=3c99d49b6af8

# Cardano (ADA)
ADA_ADDRESSES_REGEX_PATTERNS = {
    # В тексте
    'ADA address': re.compile(r'[^a-z0-9A-Z/]addr1[a-z0–9][^a-z0-9A-Z]', re.M | re.S),

    # Слово целиком
    'ADA address full': re.compile(r'addr1[a-z0–9]', re.M | re.S)
}
# ATOM
ATOM_ADDRESSES_REGEX_PATTERNS = {
    # В тексте
    'ATOM address': re.compile(r'[^a-z0-9A-Z/]cosmos[a-zA-Z0–9_.-]{10,}[^a-z0-9A-Z]', re.M | re.S),

    # Слово целиком
    'ATOM address full': re.compile(r'cosmos[a-zA-Z0–9_.-]{10,}', re.M | re.S)
}

# DOGE
DOGE_ADDRESSES_REGEX_PATTERNS = {
    # В тексте
    'DOGE address': re.compile(r'[^a-z0-9A-Z/]\sD[a-zA-Z0–9_.-]{33}[^a-z0-9A-Z]', re.M | re.S),

    # Слово целиком
    'DOGE address full': re.compile(r'\sD[a-zA-Z0–9_.-]{33}', re.M | re.S)
}

# IOTA (MIOTA)
MIOTA_ADDRESSES_REGEX_PATTERNS = {
    # В тексте
    'MIOTA address': re.compile(r'[^a-z0-9A-Z/]iota[a-z0–9]{10,}[^a-z0-9A-Z]', re.M | re.S),

    # Слово целиком
    'MIOTA address full': re.compile(r'iota[a-z0–9]{10,}', re.M | re.S)
}

# Lisk (LSK)
LSK_ADDRESSES_REGEX_PATTERNS = {
    # В тексте
    'LSK address': re.compile(r'[^a-z0-9A-Z/][0–9]{19}L[^a-z0-9A-Z]', re.M | re.S),

    # Слово целиком
    'LSK address full': re.compile(r'[0–9]{19}L', re.M | re.S)
}

# LTC
LTC_ADDRESSES_REGEX_PATTERNS = {
    # В тексте
    'LTC address': re.compile(r'[^a-z0-9A-Z/][LM3][a-km-zA-HJ-NP-Z1–9]{26,33}[^a-z0-9A-Z]', re.M | re.S),

    # Слово целиком
    'LTC address full': re.compile(r'[LM3][a-km-zA-HJ-NP-Z1–9]{26,33}', re.M | re.S)
}

# NEM (XEM)
XEM_ADDRESSES_REGEX_PATTERNS = {
    # В тексте
    'XEM address': re.compile(r'[^a-z0-9A-Z/][N][A-Za-z0–9-]{37,52}[^a-z0-9A-Z]', re.M | re.S),

    # Слово целиком
    'XEM address full': re.compile(r'[N][A-Za-z0–9-]{37,52}', re.M | re.S)
}

# NEO (NEO)
NEO_ADDRESSES_REGEX_PATTERNS = {
    # В тексте
    'NEO address': re.compile(r'[^a-z0-9A-Z/]N[0–9a-zA-Z]{33}[^a-z0-9A-Z]', re.M | re.S),

    # Слово целиком
    'NEO address full': re.compile(r'N[0–9a-zA-Z]{33}', re.M | re.S)
}

# Ontology (ONT)
ONT_ADDRESSES_REGEX_PATTERNS = {
    # В тексте
    'ONT address': re.compile(r'[^a-z0-9A-Z/]A[0–9a-zA-Z]{33}[^a-z0-9A-Z]', re.M | re.S),

    # Слово целиком
    'ONT address full': re.compile(r'A[0–9a-zA-Z]{33}', re.M | re.S)
}

# Polkadot(DOT)
DOT_ADDRESSES_REGEX_PATTERNS = {
    # В тексте
    'DOT address': re.compile(r'[^a-z0-9A-Z/]1[0–9a-zA-Z]{47}[^a-z0-9A-Z]', re.M | re.S),

    # Слово целиком
    'DOT address full': re.compile(r'1[0–9a-zA-Z]{47}', re.M | re.S)
}

# Ripple (XRP)
XRP_ADDRESSES_REGEX_PATTERNS = {
    # В тексте
    'XRP address': re.compile(r'[^a-z0-9A-Z/]r[0–9a-zA-Z]{33}[^a-z0-9A-Z]', re.M | re.S),

    # Слово целиком
    'XRP address full': re.compile(r'r[0–9a-zA-Z]{33}', re.M | re.S)
}
# Stellar (XLM)
XLM_ADDRESSES_REGEX_PATTERNS = {
    # В тексте
    'XLM address': re.compile(r'[^a-z0-9A-Z/]G[0–9A-Z]{40,60}[^a-z0-9A-Z]', re.M | re.S),

    # Слово целиком
    'XLM address full': re.compile(r'G[0–9A-Z]{40,60}', re.M | re.S)
}

# Universal (ETC, USDT, XRP, AAVE, REP, BAND, BAT, LINK, CHZ, COMP, KNC, MKR, OCEAN, OMG, PAN, REN, SNX, UMA, UNI, USDC, YFI, ZRX, 1INCH ....)
UNIVERSAL_ADDRESSES_REGEX_PATTERNS = {
    # В тексте
    'UNIVERSAL address': re.compile(r'[^a-z0-9A-Z/]0x[a-fA-F0–9]{40}$[^a-z0-9A-Z]', re.M | re.S),

    # Слово целиком
    'UNIVERSAL address full': re.compile(r'0x[a-fA-F0–9]{40}$', re.M | re.S),

}

# TRON (TRC-20)
TRC_20_ADDRESSES_REGEX_PATTERNS = {
    # В тексте
    'TRC_20 address': re.compile(r'[^a-z0-9A-Z/]^T[A-Za-z0-9]{33}$[^a-z0-9A-Z]', re.M | re.S),

    # Слово целиком
    'TRC_20 address full': re.compile(r'^T[A-Za-z0-9]{33}$', re.M | re.S),
}

# TRX (Tron)
TRX_ADDRESSES_REGEX_PATTERNS = {
    # В тексте
    'TRC_20 address': re.compile(r'[^a-z0-9A-Z/]^T[1-9a-km-zA-HJ-NP-Z]{33}$[^a-z0-9A-Z]', re.M | re.S),

    # Слово целиком
    'TRC_20 address full': re.compile(r'^T[1-9a-km-zA-HJ-NP-Z]{33}$', re.M | re.S),
}

# Словарь всех паттернов
PATTERNS = {
    CryptoName.BTC: BTC_ADDRESSES_REGEX_PATTERNS,
    CryptoName.ETH: ETH_ADDRESSES_REGEX_PATTERNS,
    CryptoName.DASH: DASH_ADDRESSES_REGEX_PATTERNS,
    CryptoName.XMR: XMR_ADDRESSES_REGEX_PATTERNS,
    CryptoName.ADA: ADA_ADDRESSES_REGEX_PATTERNS,
    CryptoName.ATOM: ATOM_ADDRESSES_REGEX_PATTERNS,
    CryptoName.DOGE: DOGE_ADDRESSES_REGEX_PATTERNS,
    CryptoName.MIOTA: MIOTA_ADDRESSES_REGEX_PATTERNS,
    CryptoName.LSK: LSK_ADDRESSES_REGEX_PATTERNS,
    CryptoName.LTC: LTC_ADDRESSES_REGEX_PATTERNS,
    CryptoName.XEM: XEM_ADDRESSES_REGEX_PATTERNS,
    CryptoName.NEO: NEO_ADDRESSES_REGEX_PATTERNS,
    CryptoName.ONT: ONT_ADDRESSES_REGEX_PATTERNS,
    CryptoName.DOT: DOT_ADDRESSES_REGEX_PATTERNS,
    CryptoName.XRP: XRP_ADDRESSES_REGEX_PATTERNS,
    CryptoName.XLM: XLM_ADDRESSES_REGEX_PATTERNS,
    CryptoName.TRC_20: TRC_20_ADDRESSES_REGEX_PATTERNS,
    CryptoName.TRX: TRX_ADDRESSES_REGEX_PATTERNS,
    CryptoName.UNIVERSAL: UNIVERSAL_ADDRESSES_REGEX_PATTERNS

}


class CryptoAddressParser:

    def __init__(self, context_size: int = 1024):
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

    def __get_context_from_text(self, text: str, html: str, target: str):
        """
        Находит контекст в text, в котором был найден target
        Если в тексте нет target - возвращает путую строку
        :param text: текст, в котором найден адрес
        :param html: исходная HTML страница
        :param target: слово, вокруг которого нужно взять контекст
        :return: контекст
        """
        text = re.sub(" +", " ", text)  # Убираем лишние пробелы
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

    def get_web_context(self, text: str, html: str, target: str):
        """
        Находит в text тег HTML в котором указан target.
        :param text: текст, в котором осуществлять поиск
        :param html: исходная HTML страница
        :param target: искомое слово
        :return: Список всех тегов с содержимым на странице, где есть target
        Если в тексте не нашёлся target - возвращает пустой список
        """
        found = ''
        soup = BeautifulSoup(html, 'html.parser')
        child_soup = soup.find_all('p')
        for i in child_soup:
            if target in i.text:
                found += ' '.join(i.text.replace("\n", " ").split())
                found += '\n---------------------------------------\n'
        if found == '':
            logging.warn(f'Не удалось обнаружить элемент {target} на странице {html} в искомых тегах')
            return text
        return found

    def __validate_address(self, address: str, crypto_name: CryptoName):
        # TODO: Дописать
        """
        Проверяет валидный ли адрес
        :param address: адрес
        :return: валидный или нет(или не удалось проверить валидность)
        """
        return False

    def __cat_not_address_symbols(self, address: str):
        """
        Обрезает крайний левый и крайний правый символы адреса, если они не являются числом или буквой
        :param address: адрес
        :return: обрезанный адрес
        """
        while address and not address[0].isalnum():  # Проверяем левый край
            address = address[1:]
        while address and not address[-1].isalnum():  # Проверяем правый край
            address = address[:-1]
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
                    address = self.__cat_not_address_symbols(word)
                    found_list.append(
                        CheckCryptoResponse(
                            crypto_name,
                            pattern_name,
                            address,
                            valid_address=self.__validate_address(address, crypto_name)
                        ))
        return found_list

    def check_is_text_contains_crypto(self, text: str, html: str, source: str = ''):
        """
        Проверяет содержится ли в тексте какой-либо известный крипто адрес
        :param text: text, в котором нужно осуществлять поиск
        :param html: html, исходная страница, в которой нужно осуществлять поиск
        :param source: источник, в котором был найден текст (ссылка на статью, ТГ канал и пр)
        :return: список найденных адресов (list of CheckCryptoResponse)
        """
        found_list_rs = []
        for crypto_name, pattern_dict in PATTERNS.items():
            for pattern_name, pattern in pattern_dict.items():
                found = self.__checkIfTextHasPattern(pattern, text)
                if len(found) != 0:
                    for f in found:
                        found_list_rs.append(
                            CheckCryptoResponse(
                                crypto_name,
                                pattern_name,
                                self.__cat_not_address_symbols(f),
                                self.get_web_context(text, html, f),
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

    # отдельная проверка конкретного слова, является ли оно крипто адресом
    crypto_parser = CryptoAddressParser()
    # Позитивный кейс
    result = crypto_parser.check_is_word_any_crypto('33yPjjSMGHPp8zj1ZXySNJzSUfVSbpXEuL')
    print('Слово является крипто адресом = ' + str(result))
    # Неготивный кейс
    result = crypto_parser.check_is_word_any_crypto('asd3yPjjSMGHPp8zj1ZXySNJzSUfVSbpXEuL')
    print('Слово НЕ является крипто адресом = ' + str(result))
