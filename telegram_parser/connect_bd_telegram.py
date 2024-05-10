import asyncpg

# Функция для сохранения данных в базу данных PostgreSQL
async def save_to_postgresql(data):
    conn = await asyncpg.connect(user='your_user', password='your_password',
                                  database='your_database', host='your_host')

    for item in data:
        await conn.execute('INSERT INTO your_table (id, title, type, link) VALUES ($1, $2, $3, $4)',
                           item['id'], item['title'], item['type'], item['link'])

    await conn.close()