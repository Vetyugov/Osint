import enum
# для regex
import re


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

    def __init__(self, crypto_Name: CryptoName, pattern_Name: str, address: str):
        self.crypto_Name = crypto_Name
        self.pattern_Name = pattern_Name
        self.address = address

    def __str__(self):
        return self.crypto_Name.name + " - " + self.pattern_Name + 'address = ' + self.address

    def __repr__(self):
        return self.crypto_Name.name + " - " + self.pattern_Name + 'address = ' + self.address


# Паттерны для адресов Биткоина
BTC_ADDRESSES_REGEX_PATTERNS = {
    'BTC Legacy address': re.compile('1[a-z0-9A-Z]{25,33}'),
    'BTC P2SH address': re.compile('3[a-z0-9A-Z]{25,33}'),
    'BTC Segwit address': re.compile('bc1[a-z0-9A-Z]{23,42}'),
    'BTC Taproot address': re.compile('bc1p[a-z0-9A-Z]{23,42}')
}

# Паттерны для адресов Эфира
ETH_ADDRESSES_REGEX_PATTERNS = {
    # All Ethereum addresses have a length of 40 hexadecimal characters and begin with “0x”
    'ETH address': re.compile('0x[0-9A-Fa-f]{40}')
}

# Словарь всех паттернов
PATTERNS = {
    CryptoName.BTC: BTC_ADDRESSES_REGEX_PATTERNS,
    CryptoName.ETH: ETH_ADDRESSES_REGEX_PATTERNS
}


# TODO: Дополнить списки


def check_if_string_contains_substring_by_regex(regex: str):
    return None


def check(pattern, word: str):
    """

    :param pattern: паттерн Pattern из библиотеки re
    :param word: слово, которое анализируем
    :return: результат true/false
    """
    is_match = re.match(pattern, word)
    # TODO тут можно обрезать ковыки/точки в конце и начале слова, чтобы улучшить результат
    return is_match


def check_is_word_BTC_crypto_address(word: str):
    """
    Проверяет, удовлетворяет ли слово паттерну
    :param word: слово, которое анализируем
    :return: результат
    """
    for pattern_name, pattern in BTC_ADDRESSES_REGEX_PATTERNS.items():
        if check(pattern, word):
            return pattern_name
    return None


def check_is_word_ETH_crypto_address(word: str):
    for pattern_name, pattern in ETH_ADDRESSES_REGEX_PATTERNS.items():
        if check(pattern, word):
            return pattern_name
    return None


def check_is_word_specific_crypto(word: str, crypto_name: CryptoName):
    if crypto_name == CryptoName.BTC:
        return check_is_word_BTC_crypto_address(word)
    if crypto_name == CryptoName.ETH:
        return check_is_word_ETH_crypto_address(word)


def check_is_word_any_crypto(word: str):
    """
    Проверяет, соответствует ли слово хотя бы одному известному шаблону
    :param word: проверяемое слово
    :return: результат проверки. None в случае не соотвтетсвия ни одному шаблону
    """
    for crypto_name, pattern_dict in PATTERNS.items():
        for pattern_name, pattern in pattern_dict.items():
            if check(pattern, word):
                return CheckCryptoResponse(crypto_name, pattern_name, word)
    return None
