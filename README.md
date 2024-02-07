# ylab-fastapi-postgresql

Для работы необходим docker.

Настройка происходит в файле .env его нет в репозитории, т.к. он конфиденциален, но я предоставил файл .env.dist создайте на его основе файл .env и проведите все необходимые настройки.

Запуск приложения осуществляется командой:
> docker-compose up -d
>

Запуск тестов производится командой:
> docker-compose -f docker-compose-tests.yaml up --exit-code-from tests_restaurant_ylab
>
