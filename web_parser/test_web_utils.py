from web_utils import get_static_html_from, get_text_from_html, get_dynamic_html_from

if __name__ == '__main__':
    text = get_text_from_html(get_static_html_from("https://bits.media/price/bnb/usdt/"))
    print(text)
#
#
# if __name__ == '__main__':
#     text = get_html_from("https://www.crummy.com/software/BeautifulSoup/bs4/doc/")
#     print(text)

# get_dynamic_html_from("https://www.crummy.com/software/BeautifulSoup/bs4/doc/")


