import sqlite3
from datetime import datetime


class WebParsedLink:
    def __init__(self, id, link: str, link_from: str, last_monitoring_time: datetime):
        self.id = id
        self.link = link
        self.link_from = link_from
        self.last_monitoring_time = last_monitoring_time


class WebFoundAddress:
    def __init__(self, id, crypto_name: str, pattern_name: str, address: str, context: str, source: str,
                 found_time: datetime):
        self.id = id
        self.crypto_name = crypto_name
        self.pattern_name = pattern_name
        self.address = address
        self.context = context
        self.source = source
        self.found_time = found_time


class WebSourceLink:
    def __init__(self, id, link: str, analyzed):
        self.id = id
        self.link = link
        self.analyzed = analyzed


class DataBaseService:
    def __init__(self, source: str):
        # Создаем подключение к базе данных (файл source будет создан)
        self.connection = sqlite3.connect(source)
        self.create_tables()
        return

    def close_connection(self):
        self.connection.close()

    def create_tables(self):
        cursor = self.connection.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS web_parsed_link (      id INTEGER PRIMARY KEY,
                                                          link TEXT NOT NULL,
                                                          link_from TEXT DEFAULT '',
                                                          last_monitoring_time TEXT
        );
        ''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS web_found_address (  id INTEGER PRIMARY KEY,
                                                          crypto_name TEXT NOT NULL,
                                                          pattern_name TEXT NOT NULL,
                                                          address TEXT NOT NULL,
                                                          context TEXT,
                                                          source TEXT,
                                                          found_time TEXT
        );
        ''')
        cursor.execute('''
                CREATE TABLE IF NOT EXISTS web_sources_links (  id INTEGER PRIMARY KEY,
                                                                  link TEXT NOT NULL,
                                                                  analyzed_time TEXT
                );
                ''')

        # Сохраняем изменения
        self.connection.commit()

    def get_all_links_for_analize(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM web_sources_links WHERE analyzed_time IS NULL OR STRFTIME(\'%Y-%m-%d\', analyzed_time) < (STRFTIME(\'%Y-%m-%d\', CURRENT_DATE) - INTERVAL \'1 day\')')
        web_sources_links = cursor.fetchall()
        return [WebSourceLink(link[0], link[1], link[2]) for link in web_sources_links]

    def get_all_parsed_links(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM web_parsed_link')
        web_parsed_link = cursor.fetchall()
        return [WebParsedLink(link[0], link[1], link[2], link[3]) for link in web_parsed_link]

    def is_link_already_parsed(self, link: str):
        cursor = self.connection.cursor()
        cursor.execute(f'SELECT * FROM web_parsed_link where link = \'{link}\' ')
        web_parsed_link = cursor.fetchall()
        return len(web_parsed_link) > 0

    def save_new_parsed_link(self, new: WebParsedLink):
        cursor = self.connection.cursor()
        cursor.execute(
            'INSERT INTO web_parsed_link (id, link,link_from,last_monitoring_time) VALUES (NULL, ?, ?, ?)',
            (new.link, new.link_from, new.last_monitoring_time.strftime("%Y-%m-%d %H-%M-%S")))
        self.connection.commit()

    def get_all_found_addresses(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM web_found_address')
        web_found_addresses = cursor.fetchall()
        return [WebFoundAddress(link[0], link[1], link[2], link[3], link[4], link[5], link[6]) for link in
                web_found_addresses]

    def save_new_found_address(self, new: WebFoundAddress):
        cursor = self.connection.cursor()
        cursor.execute(
            'INSERT INTO web_found_address (crypto_name, pattern_name, address, context, source, found_time) VALUES (?, ?, ?, ?, ?, ?)',
            (new.crypto_name, new.pattern_name, new.address, new.context, new.source,
             new.found_time.strftime("%Y-%m-%d %H-%M-%S"),))
        self.connection.commit()


if __name__ == '__main__':
    db = DataBaseService(source='./web_monitoring.sqlite')
    db.create_tables()
    db.close_connection()
