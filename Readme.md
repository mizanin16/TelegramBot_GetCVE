# Telegram Bot Get CVE

## Алгоритм выполненной работы.
1. Скачан файл уязвимостей с сайта [Сайт для скачивания!](https://bdu.fstec.ru/vul).
2. Добавлена вся информация по уязвимостям из файла в базу данных sqlite3.
3. Зарегистрирован бот в Телеграмме через аккаунт @BotFather.
4. Написан каркас для обращения к базе данных из бота по разным командам с возможностью варьирования полноты отображаемой информации и количества сообщений.
5. Размещён бот на хостинге.


## Алгоритм запуска программы.
1. Установить интерпретатор Python 3.7 и выше. 
2. Переходим в рабочую папку проекта.
3. Собрать виртуальную среду для упрощенного запуска. 
**Команда:** ```python -m venv venv```
4. Активировать виртуальную среду. 
**Команда:** ```source venv/bin/activate```
5. Установить зависимости. 
**Команда:** ```pip install -r requerements.txt```
6. Скачать файл уязвимостей с сайта [Сайт для скачивания!](https://bdu.fstec.ru/vul) и сохранить в папку bd проекта.
7. Создать файл config.py с переменной TOKEN, в которой будет Telegram API ключ из @BotFather.
8. Можно запускать наш бот 
**Команда:** ```python main.py```
