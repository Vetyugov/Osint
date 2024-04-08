import csv
from connect import client
from set_parameters import keywords

async def search_channels(client, keywords):
    channels = []
    async for dialog in client.iter_dialogs():
        if dialog.is_channel:
            for keyword in keywords:
                if keyword in dialog.name.lower():
                    channels.append(dialog)
                    break
    return channels

with client:
    channels = client.loop.run_until_complete(search_channels(client, keywords))

# Запись каналов в csv файл
with open('channels.csv', mode='w', newline='', encoding='utf-8') as f:
    fieldnames = ['name']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for channel in channels:
        writer.writerow({'name': channel.name})