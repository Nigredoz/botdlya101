from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

#b1 = KeyboardButton('/Игроки')
b2 = KeyboardButton('/Данные')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

kb_client.add(b2)

