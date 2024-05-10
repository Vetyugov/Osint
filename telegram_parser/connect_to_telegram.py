import configparser
from telethon.sync import TelegramClient
def connect_to_telegram():
    # Чтение параметров из файла auth_telegram.ini
    config = configparser.ConfigParser()
    config.read('auth_telegram.ini')

    api_id = config.get('Telegram', 'api_id')
    api_hash = config.get('Telegram', 'api_hash')
    phone_number = config.get('Telegram', 'phone_number')

    # Подключение к Telegram
    client = TelegramClient('session_name', api_id, api_hash)

    # Проверка подключения к Telegram
    try:
        client.connect()
        if not client.is_user_authorized():
            client.send_code_request(phone_number)
            client.sign_in(phone_number, input('Введите код аутентификации: '))
        return client
    except Exception as e:
        print(f"Ошибка при подключении к Telegram: {e}")
        exit(1)
