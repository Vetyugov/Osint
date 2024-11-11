from bs4 import BeautifulSoup

from crypto_address_parser.address_parser import CryptoAddressParser
from web_parser.web_utils import get_text_from_html, get_response_from

if __name__ == '__main__':
    # target = '1BQ9qza7fn9snSCyJQB3ZcN46biBtkt4ee'
    url = 'https://forum.bits.media/'

    target = '0x43fa21d92141BA9db43052492E0DeEE5aa5f0A93'
    url = 'https://ofac.treasury.gov/recent-actions/20230823'
    # Reading the file
    response = get_response_from(url)

    crypto_address_parser = CryptoAddressParser()

    print(crypto_address_parser.get_web_context('text', html, target))

    # print(footer_element)
    # while footer_element.
