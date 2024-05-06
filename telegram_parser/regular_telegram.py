import re

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
    # All Ethereum addresses have a length of 40 hexadecimal characters and begin with "0x"
    # В тексте
    'ETH address': re.compile(r'[^a-z0-9A-Z/]0x[0-9A-Fa-f]{40}[^a-z0-9A-Z]', re.M | re.S),

    # Слово целиком
    'ETH address full': re.compile(r'^0x[0-9A-Fa-f]{40}$', re.M | re.S)
}

# Словарь всех паттернов
PATTERNS = {
    'BTC': BTC_ADDRESSES_REGEX_PATTERNS,
    'ETH': ETH_ADDRESSES_REGEX_PATTERNS
}
