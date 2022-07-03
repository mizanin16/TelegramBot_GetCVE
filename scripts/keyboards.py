from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

inline_kb_full = InlineKeyboardMarkup(row_width=2)
inline_kb_full.add(InlineKeyboardButton('Короткий список', callback_data='btn1'))
inline_kb_full.add(InlineKeyboardButton('Длинный список', callback_data='btn2'))


inline_kb_count = InlineKeyboardMarkup(row_width=2)
inline_kb_count.add(InlineKeyboardButton('5 сообщений', callback_data='btn5'))
inline_kb_count.add(InlineKeyboardButton('10 сообщений', callback_data='btn6'))
inline_kb_count.add(InlineKeyboardButton('Весь список', callback_data='btn7'))
