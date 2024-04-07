import csv
import datetime
import re
import time

from telethon.tl.functions.messages import GetHistoryRequest

from connect import client
from set_parameters import groups, ethereum_pattern, bitcoin_pattern

# Открываем CSV файл для записи ссылок на посты
with open('telegram_osint.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Group', 'Post Link', 'Ethereum Addresses', 'Bitcoin Addresses', 'Time Posted', 'Count'])

    for group in groups:
        # Получение истории сообщений из каждой группы с задержкой в 60 секунд
        time.sleep(60)
        channel_entity = client.get_entity(group)
        messages = client(GetHistoryRequest(peer=channel_entity, limit=500, offset_date=None, offset_id=0, max_id=0, min_id=0, add_offset=0, hash=0))

        ethereum_address_count = {}
        bitcoin_address_count = {}
        # Поиск сообщений, содержащих Ethereum-адреса и Bitcoin-адреса и запись их в CSV файл
        for message in messages.messages:
            if message.message:
                ethereum_addresses = re.findall(ethereum_pattern, message.message)
                bitcoin_addresses = re.findall(bitcoin_pattern, message.message)
                post_time = datetime.datetime.utcfromtimestamp(message.date).strftime('%Y-%m-%d %H:%M:%S') if isinstance(message.date, int) else message.date.strftime('%Y-%m-%d %H:%M:%S')
                post_title = message.post
                for address in ethereum_addresses:
                    post_link = f"https://t.me/{group}/{message.id}"
                    writer.writerow([group, post_link, address, '', post_time])
                    ethereum_address_count[address] = ethereum_address_count.get(address, 0) + 1
                for address in bitcoin_addresses:
                    post_link = f"https://t.me/{group}/{message.id}"
                    writer.writerow([group, post_link, '', address, post_time])
                    bitcoin_address_count[address] = bitcoin_address_count.get(address, 0) + 1

        sorted_ethereum_addresses = sorted(ethereum_address_count.items(), key=lambda x: x[1], reverse=True)
        sorted_bitcoin_addresses = sorted(bitcoin_address_count.items(), key=lambda x: x[1], reverse=True)

        for address, count in sorted_ethereum_addresses:
            print(f"Ethereum Address: {address}, Count: {count}")

        for address, count in sorted_bitcoin_addresses:
            print(f"Bitcoin Address: {address}, Count: {count}")

