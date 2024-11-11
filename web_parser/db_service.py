from datetime import datetime

import psycopg2


class WebParsedLink:
    def __init__(self, id, link: str, link_from: str, last_monitoring_time: datetime):
        self.id = id
        self.link = link
        self.link_from = link_from
        self.last_monitoring_time = last_monitoring_time


class WebFoundAddress:
    def __init__(self, id, crypto_name: str, pattern_name: str, address: str, context: str, source: str,
                 found_time: datetime, valid_address: bool):
        self.id = id
        self.crypto_name = crypto_name
        self.pattern_name = pattern_name
        self.address = address
        self.context = context
        self.source = source
        self.found_time = found_time
        self.valid_address = valid_address


class WebSourceLink:
    def __init__(self, id, link: str, analyzed_time, active: bool = True):
        self.id = id
        self.link = link
        self.analyzed_time = analyzed_time
        self.active = active

    def __repr__(self):
        return 'id = ' + str(self.id) + ' , link = ' + self.link + ',  active = ' + str(self.active)

    def __str__(self):
        return 'id = ' + str(self.id) + ' , link = ' + self.link + ',  active = ' + str(self.active)


SQLITE_FILE_PATH = './web_monitoring.sqlite'
POSTGRES_URL = 'postgresql://osint_admin:osint_admin@localhost:5431/osint_db'


class DataBaseService:
    def __init__(self):
        # Создаем подключение к базе данных (файл source будет создан)
        # self.connection = sqlite3.connect(SQLITE_FILE_PATH)

        try:
            # пытаемся подключиться к базе данных
            self.connection = psycopg2.connect(POSTGRES_URL)
        except:
            # в случае сбоя подключения будет выведено сообщение  в STDOUT
            print('Can`t establish connection to database')
        return

    def close_connection(self):
        self.connection.close()

    def get_all_links_for_analize(self):
        """
        :return: Возвращает ссылки, которые необходимо проанализировать (флаг active = true)
        """
        cursor = self.connection.cursor()
        # cursor.execute('SELECT * FROM osint_web.web_sources_links WHERE analyzed_time IS NULL OR STRFTIME(\'%Y-%m-%d\', analyzed_time) < (STRFTIME(\'%Y-%m-%d\', CURRENT_DATE) - INTERVAL \'1 day\')')
        cursor.execute('SELECT * FROM osint_web.web_sources_links WHERE active = true')
        web_sources_links = cursor.fetchall()
        return [WebSourceLink(link[0], link[1], link[2], link[3]) for link in web_sources_links]

    # def get_all_parsed_links(self):
    #     cursor = self.connection.cursor()
    #     cursor.execute('SELECT * FROM osint_web.web_parsed_link')
    #     web_parsed_link = cursor.fetchall()
    #     return [WebParsedLink(link[0], link[1], link[2], link[3]) for link in web_parsed_link]
    #
    # def is_link_already_parsed(self, link: str):
    #     cursor = self.connection.cursor()
    #     cursor.execute(f'SELECT * FROM osint_web.web_parsed_link where link = \'{link}\' ')
    #     web_parsed_link = cursor.fetchall()
    #     return len(web_parsed_link) > 0

    def get_not_parsed_links(self, links: list):
        cursor = self.connection.cursor()
        cursor.execute(f'SELECT * FROM osint_web.web_parsed_link where link in {tuple(links)} ')
        web_parsed_links = [link[1] for link in cursor.fetchall()]
        return [link for link in links if link not in web_parsed_links]

    def save_new_parsed_link(self, new: WebParsedLink):
        cursor = self.connection.cursor()
        cursor.execute(
            'INSERT INTO osint_web.web_parsed_link (link,link_from, last_monitoring_time) VALUES (%s, %s, %s)',
            (new.link, new.link_from, new.last_monitoring_time))
        self.connection.commit()

    # def get_all_found_addresses(self):
    #     cursor = self.connection.cursor()
    #     cursor.execute('SELECT * FROM osint_web.web_found_address')
    #     web_found_addresses = cursor.fetchall()
    #     return [WebFoundAddress(link[0], link[1], link[2], link[3], link[4], link[5], link[6], link[7]) for link in
    #             web_found_addresses]

    def save_new_found_address(self, new: WebFoundAddress):
        cursor = self.connection.cursor()
        cursor.execute(
            'INSERT INTO osint_web.web_found_address (crypto_name, pattern_name, address, context, source, found_time, valid_address) VALUES (%s, %s, %s, %s, %s, %s, %s)',
            (new.crypto_name, new.pattern_name, new.address, new.context, new.source,
             new.found_time.strftime("%Y-%m-%d %H:%M:%S"), new.valid_address))
        self.connection.commit()


if __name__ == '__main__':
    db = DataBaseService()
    db.close_connection()
