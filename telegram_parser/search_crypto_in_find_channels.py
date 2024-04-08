import csv
import datetime
import re
import asyncio
import telethon
from set_parameters import Parameters
from connect import client
import search_channels

class SearchCryptoInFindChannels:
    async def search(self):
        ethereum_pattern = Parameters.ethereum_pattern
        bitcoin_pattern = Parameters.bitcoin_pattern
        keywords = Parameters.keywords
        # Открываем CSV файл для записи ссылок на посты
        with open('telegram_osint.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Group', 'Post Link', 'Ethereum Addresses', 'Bitcoin Addresses', 'Time Posted', 'Count'])

            channels = await search_channels.search_channels(client, keywords)

            for channel in channels:
                from telethon.errors import RPCError
                try:
                    channel_entity = await client.get_entity(channel)
                    messages = await client.get_messages(channel_entity, limit=500)

                    ethereum_address_count = {}
                    bitcoin_address_count = {}

                    for message in messages:
                        if message.message:
                            ethereum_addresses = re.findall(ethereum_pattern, message.message)
                            bitcoin_addresses = re.findall(bitcoin_pattern, message.message)
                            post_time = datetime.datetime.utcfromtimestamp(message.date).strftime(
                                '%Y-%m-%d %H:%M:%S') if isinstance(message.date, int) else message.date.strftime(
                                '%Y-%m-%d %H:%M:%S')
                            post_title = message.post
                            for address in ethereum_addresses:
                                post_link = f"https://t.me/{channel_entity.username}/{message.id}"
                                writer.writerow([channel_entity.name, post_link, address, '', post_time])
                                ethereum_address_count[address] = ethereum_address_count.get(address, 0) + 1
                            for address in bitcoin_addresses:
                                post_link = f"https://t.me/{channel_entity.username}/{message.id}"
                                writer.writerow([channel_entity.name, post_link, '', address, post_time])
                                bitcoin_address_count[address] = bitcoin_address_count.get(address, 0) + 1

                    sorted_ethereum_addresses = sorted(ethereum_address_count.items(), key=lambda x: x[1], reverse=True)
                    sorted_bitcoin_addresses = sorted(bitcoin_address_count.items(), key=lambda x: x[1], reverse=True)

                    for address, count in sorted_ethereum_addresses:
                        print(f"Ethereum Address: {address}, Count: {count}")

                    for address, count in sorted_bitcoin_addresses:
                        print(f"Bitcoin Address: {address}, Count: {count}")

                except RPCError as e:
                    print(f"Error with channel {channel.name}: {e}")

            await client.disconnect()
