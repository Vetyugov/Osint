import re
import json
import os
import time
from datetime import datetime

from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.functions.contacts import SearchRequest
from telethon.errors.rpcerrorlist import RpcCallFailError

from connect_to_telegram import connect_to_telegram
from connect_bd_telegram import save_to_postgresql
from telegram_parser import regular_telegram

client = connect_to_telegram()

# Определение регулярных выражений для поиска криптокошельков
ethereum_pattern = regular_telegram.PATTERNS['ETH']['ETH address']
bitcoin_pattern = regular_telegram.PATTERNS['BTC']['BTC Legacy address']

async def search_channels_and_chats(handy_search_telegram, client, keywords):
    channels_and_chats = []
    unique_chats = set()

    # Поиск по определенным каналам и чатам
    for chat in handy_search_telegram:
        try:
            entity = await client.get_entity(chat)
            if entity.megagroup or entity.broadcast:
                if entity.id not in unique_chats:
                    channels_and_chats.append(entity)
                    unique_chats.add(entity.id)
        except Exception as e:
            print(f"Ошибка при получении сущности для {chat}: {e}")

    # Поиск по ключевым словам
    for keyword in keywords:
        results = await client(SearchRequest(q=keyword, limit=100))
        for result in results.chats:
            if result.megagroup or result.broadcast:
                if result.id not in unique_chats:
                    channels_and_chats.append(result)
                    unique_chats.add(result.id)

    # Сохранение списка каналов и чатов в JSON-файл
    data = []
    for chat in channels_and_chats:
        chat_link = f"https://t.me/{chat.username}" if chat.username else f"https://t.me/{chat.id}"
        data.append({
            'id': chat.id,
            'title': chat.title,
            'type': 'Channel' if chat.broadcast else 'Chat',
            'link': chat_link
        })

    filename = 'channels_and_chats.json'
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)

    return channels_and_chats


# Функция для поиска криптокошельков в сообщениях
async def search_crypto_wallets(chat_entity):
    wallets_found = []
    chat_name = f"{chat_entity.title} ({chat_entity.id})"
    last_message_id = 0
    retries = 3  # Количество повторных попыток
    while True:
        try:
            messages = await client(GetHistoryRequest(
                peer=chat_entity,
                limit=100,
                offset_id=last_message_id,
                min_id=0,
                max_id=0,
                add_offset=0,
                offset_date=datetime.now(),
                hash=0
            ))
            if not messages.messages:
                break
            for message in messages.messages:
                text = message.message
                if text:
                    post_link = f"https://t.me/{chat_entity.username}/{message.id}" if chat_entity.username else f"https://t.me/c/{chat_entity.id}/{message.id}"
                    ethereum_wallets = re.findall(ethereum_pattern, text)
                    bitcoin_wallets = re.findall(bitcoin_pattern, text)
                    if ethereum_wallets:
                        wallets_found.append({
                            "chat_name": chat_name,
                            "post_link": post_link,
                            "post_id": message.id,
                            "cryptocurrency": "Ethereum",
                            "wallets": ethereum_wallets
                        })
                    if bitcoin_wallets:
                        wallets_found.append({
                            "chat_name": chat_name,
                            "post_link": post_link,
                            "post_id": message.id,
                            "cryptocurrency": "Bitcoin",
                            "wallets": bitcoin_wallets
                        })
            last_message_id = messages.messages[-1].id
        except RpcCallFailError as e:
            if retries > 0:
                print(f"Ошибка при получении сообщений для {chat_name}: {e}. Повторная попытка...")
                retries -= 1
                time.sleep(5)  # Ждем 5 секунд перед повторной попыткой
            else:
                print(f"Достигнуто максимальное количество повторных попыток для {chat_name}. Пропускаем.")
                break
        except Exception as e:
            print(f"Ошибка при получении сообщений для {chat_name}: {e}")
            break
    return wallets_found


# Функция для выгрузки данных в формате JSON
async def export_to_json(chat_entity):
    start_time = time.time()
    wallets_found = await search_crypto_wallets(chat_entity)
    if wallets_found:
        chat_name = f"{chat_entity.title} ({chat_entity.id})"
        # Создание папки "osint" если она не существует
        if not os.path.exists("osint"):
            os.makedirs("osint")

        filename = os.path.join("osint", ''.join(
            c for c in chat_name if c.isalnum() or c in ' _-').rstrip() + '_crypto_data.json')
        with open(filename, 'w', encoding='utf-8') as json_file:
            json.dump(wallets_found, json_file, indent=4, ensure_ascii=False)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Поиск и выгрузка данных для {chat_name} завершены за {execution_time} секунд")

# Функция для выгрузки данных в базу данных PostgreSQL
async def export_to_postgresql(chat_entity):
    start_time = time.time()
    wallets_found = await search_crypto_wallets(chat_entity)
    if wallets_found:
        await save_to_postgresql(wallets_found)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Поиск и выгрузка данных для завершены за {execution_time} секунд")