import time
import regular_telegram
from connect_to_telegram import connect_to_telegram
from read_file_for_telegram import read_files_for_telegram
from telegram_parser.main_func_telegram import search_channels_and_chats, export_to_json, client

if __name__ == "__main__":
    # Подключение к Telegram

    # Чтение списка каналов и чатов, а также ключевых слов
    handy_search_telegram, keywords = read_files_for_telegram()

    # Общее время выполнения
    total_start_time = time.time()

    # Поиск каналов и чатов по ключевым словам, каналам и чатам
    channels_and_chats = client.loop.run_until_complete(search_channels_and_chats(handy_search_telegram, client, keywords))

    # Запуск поиска и выгрузки данных для каждого канала и чата
    for chat in channels_and_chats:
        client.loop.run_until_complete(export_to_json(chat))

    total_end_time = time.time()
    total_execution_time = total_end_time - total_start_time
    print(f"Общее время выполнения: {total_execution_time} секунд")

    # Отключение от Telegram
    client.disconnect()
