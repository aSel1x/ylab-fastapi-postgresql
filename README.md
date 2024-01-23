# ylab-fastapi-postgresql
В директории ylab необходимо создать виртуальное окружение, используя команду:
> python3 -m venv venv
>
Затем активировать его, используя:
> source venv/bin/activate
>
Далее необходимо установить библиотеки, необходимые для работы проекта: 
> pip install -r requirements.txt
>

Запуск производится командой:
> python3 -m app -db-url YOUR_DB_URL  -db-prt YOUR_DB_PORT -db-name YOUR_DB_NAME -db-usr YOUR_DB_USER -db-pwd YOUR_DB_PASSWORD
>