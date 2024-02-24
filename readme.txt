1) Виртуальная среда питон:
создание вирт среды
python -m venv .venv
активация
.venv\Scripts\activate
деактивация
deactivate
установка зависимостей
pip install -r freeze.txt
2)докер
https://blog.ithillel.ua/ru/articles/sovety-po-startu-proekta-na-django-i-docker
3) admin 1234
4) python manage.py inspectdb > models.py создание моделей бд
5) генерация requirements 
pip freeze > freeze.txt
6) настройка vscode 
mkdir .vscode
7)  python manage.py runserver 192.168.6.168:8000
8) для лены:
    ссылка на фронте:
    # http://127.0.0.1:8001 на работе со своего
    # http://192.168.6.168:8001 на работе с вероникиного
    # http://127.0.0.1:8000 дома
    python -m venv .venv
    .venv\Scripts\activate
    cd LAMA_ucup
    python manage.py runserver 8001 
    или 
    python manage.py runserver
9) миграции:
 python manage.py makemigrations
 python manage.py migrate