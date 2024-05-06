import time
import regular_telegram
from connect_to_telegram import connect_to_telegram
from read_file_for_telegram import read_files_for_telegram
from main_func_telegram import search_channels_and_chats, export_to_json

if __name__ == "__main__":
    # Подключение к Telegram
    client = connect_to_telegram()

    # Определение регулярных выражений для поиска криптокошельков
    ethereum_pattern = regular_telegram.PATTERNS['ETH']['ETH address']
    bitcoin_pattern = regular_telegram.PATTERNS['BTC']['BTC Legacy address']

    # Чтение списка каналов и чатов, а также ключевых слов
    handly_search, keywords = read_files_for_telegram()

    # Общее время выполнения
    total_start_time = time.time()

    # Поиск каналов и чатов по ключевым словам, каналам и чатам
    channels_and_chats = client.loop.run_until_complete(search_channels_and_chats())

    # Запуск поиска и выгрузки данных для каждого канала и чата
    for chat in channels_and_chats:
        client.loop.run_until_complete(export_to_json(chat))

    total_end_time = time.time()
    total_execution_time = total_end_time - total_start_time
    print(f"Общее время выполнения: {total_execution_time} секунд")

    # Отключение от Telegram
    client.disconnect()
