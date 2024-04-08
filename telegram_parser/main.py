import time
import asyncio
from connect import client
from search_crypto_in_find_channels import SearchCryptoInFindChannels

if __name__ == "__main__":
    start_time = time.time()
    async def run():
        await client.start()
        search_crypto = SearchCryptoInFindChannels()
        await search_crypto.search()
        await client.disconnect()

    asyncio.run(run())

    end_time = time.time()  # Засекаем время окончания выполнения кода
    execution_time = end_time - start_time
    print(f"Время выполнения: {execution_time} секунд(-ы)")