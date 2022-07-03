import os.path

from scripts.connection import get_info_fetchall
from aiogram import Bot, Dispatcher, executor, types
import scripts.keyboards as kb
import time
from scripts.config import TOKEN
from scripts.open_xls import file_db, to_sql_excel, data_set

# Объект бота
bot = Bot(token=TOKEN)
# Диспетчер для бота
dp = Dispatcher(bot)

# Задаём глобальные default переменные для бота
length_msg = 1
count_msg = 5


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('btn'))
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    """
    Обработка кнопок
    """
    code = callback_query.data[-1]
    global length_msg
    global count_msg

    if code.isdigit():
        code = int(code)
    if code == 1:
        length_msg = 1
        await bot.answer_callback_query(callback_query.id, text='Применен короткий вывод!')
    elif code == 2:
        length_msg = 2
        await bot.answer_callback_query(callback_query.id, text='Применен полный вывод!')

    elif code == 5:
        count_msg = 5
        await bot.answer_callback_query(callback_query.id, text='Применено 5 сообщений для вывода!')
    elif code == 6:
        count_msg = 10
        await bot.answer_callback_query(callback_query.id, text='Применено 10 сообщений для вывода!')
    elif code == 7:
        count_msg = 0
        await bot.answer_callback_query(callback_query.id, text='Применены сообщения без огрпничений для вывода!')


@dp.message_handler(commands=['TypeMsg'])
async def process_command_1(message: types.Message):
    await message.reply("Выберете тип отображения сообщения", reply_markup=kb.inline_kb_full)


@dp.message_handler(commands=['CountMsg'])
async def process_command_2(message: types.Message):
    await message.reply("Выберете количество сообщений", reply_markup=kb.inline_kb_count)


@dp.message_handler(commands=['help', 'start'])
async def send_welcome(msg: types.Message):
    """
    Ответ на сообщение /help и /start
    """
    # Отправка пояснительной информации
    text_to_answer = '<b>Здравствуйте!</b>\nДанный бот выполняет запрос в БД уязвимостей ' \
                     'в зависимости от запрашиваемой команды инфорамации.\n' \
                     r'Для полной информации о доступных командах введите /commands'
    await msg.answer(text_to_answer, parse_mode='HTML')


@dp.message_handler(commands="commands")
async def send_commands(message: types.Message):
    """
    Ответ на сообщение /commands
    Доступный список комманд
    """
    text_to_answer = '/help - стартовое сообщение\n' \
                     '/CountMsg - количество сообщений для отображения\n' \
                     '/TypeMsg - тип вывода сообщений\n' \
                     '#TypeSystem - Тип системы\n' \
                     '#NameProgramm - Имя программного продукта\n' \
                     '#NameVulnerability - Наименование уязвимости\n' \
                     '<b>ПРИМЕР</b>: #TypeSystem Windows\n' \
                     '<b>ПРИМЕР</b>: #NameProgramm Google Chrome'
    await message.answer(text_to_answer, parse_mode='HTML')


@dp.message_handler()
async def send_welcome(msg: types.Message):
    """
    Получаем сообщение Боту и производим соотношение команд
    """
    list_find = ['#TypeSystem', '#NameProgramm', '#NameVulnerability']
    for type_find in list_find:
        if type_find.title() in msg.text.title():
            # Оставляем только условие для поиска
            title = msg.text
            title = title.replace(type_find, '')
            # Делаем запрос в БД
            rows = get_info_fetchall(title, type_where=type_find)
            if count_msg > 0:
                # Ограничиваем количество вывода
                rows = rows[:count_msg]
            for row in rows:
                if length_msg == 2:
                    # Отправка сообщения при подробном отображении
                    text_to_answer = f'<b>Идентификатор:</b> {row[0]}\n' \
                                     f'<b>Наименование уязвимости:</b> {row[1]}\n' \
                                     f'<b>Описание уязвимости:</b> {row[2]}\n' \
                                     f'<b>Вендор ПО:</b> {row[3]}\n' \
                                     f'<b>Название ПО:</b> {row[4]}\n' \
                                     f'<b>Версия ПО:</b> {row[5]}\n' \
                                     f'<b>Тип ПО:</b> {row[6]}\n' \
                                     f'<b>Наименование ОС и тип аппаратной платформы:</b> {row[7]}\n' \
                                     f'<b>Возможные меры по устранению:</b> {row[13]}\n' \
                                     f'<b>Ссылки на источники:</b> {row[17]}\n' \
                                     f'<b>Идентификаторы других систем описаний уязвимости:</b> {row[18]}\n' \
                                     f'<b>Тип ошибки CWE:</b> {row[21]}\n'
                else:
                    # Отправка сообщения при коротком отображении
                    text_to_answer = f'<b>Идентификатор:</b> {row[0]}\n' \
                                     f'<b>Описание уязвимости:</b> {row[2]}\n'
                await msg.answer(text_to_answer, parse_mode='HTML')
                # Реализовано для недопущения блокировки из-за спама
                time.sleep(2)

            if len(rows) == 0:
                # Ответ в случае отсутсвия данных
                await msg.answer('<b>Ничего не найдено!</b> Данные в БД отсутствуют', parse_mode='HTML')
            await msg.answer('<b>Успешно выполнен запрос!</b>', parse_mode='HTML')
            return
    else:
        await msg.answer('Данной команды нет в списке! Попробуйте /commands')


if __name__ == "__main__":
    while True:
        if os.path.exists(file_db):
            # Запуск бота
            executor.start_polling(dp, skip_updates=True)
        else:
            print(f'{file_db} is not exists.')
            if os.path.exists(data_set):
                print(f'Произойдёт занесение данных в БД с файла {data_set}')
                to_sql_excel()
            else:
                print(f'Скачаёте файл и положите по пути {data_set}')
                exit()
