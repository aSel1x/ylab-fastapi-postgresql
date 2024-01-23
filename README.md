# ylab-fastapi-postgresql
В директории ylab необходимо создать виртуальное окружение, используя комагды:
> python -m venv venv
>
Затем активировать его, используя:
> source venv/bin/activate
>
Далее необходимо установить библиотеки, необходимые для работы проекта: 
> pip install -r requirements.txt
> 
Перейдите в директорию:
> cd app
>

Установите переменные виртуального окружения для "DB_USER" и "DB_PASSWORD".

Запуск производится командой:
> uvicorn main:app --reload
>