### Установка Docker:
Создание докер контейнера БД
>docker run --name osint-pg-14 -p 5431:5432 -e POSTGRES_USER=osint_admin -e POSTGRES_PASSWORD=osint_admin -e POSTGRES_DB=osint_db -d postgres:14
