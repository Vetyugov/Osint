async def search_channels(client, keywords):
    channels = []
    async for dialog in client.iter_dialogs():
        if dialog.is_channel:
            for keyword in keywords:
                if keyword in dialog.name.lower():
                    channels.append(dialog)
                    break
    return channels