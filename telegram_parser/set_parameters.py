class Parameters:
    ethereum_pattern = r'\b(0x[a-fA-F0-9]{40})\b'
    bitcoin_pattern = r'\b(?:bc1|[13])[A-HJ-NP-Z0-9]{25,39}\b'
    keywords = [
        'биткоин', 'эфириум', 'криптовалюта', 'блокчейн', 'крипторасследования', 'cryptocurrency investigations', 'bitcoin',
        'etherium', 'криптобиржа', 'криптогазеты', 'криптоновости', 'криптофорум', 'криптокошельки', 'майнинг',
        'криптофермы', 'криптомошенничество', 'Криптовалюта', 'Криптоскамеры', 'Криптоскам', 'Cryptoscam',
        'Crypto fraud', 'Crypto'
    ]