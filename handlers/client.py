from aiogram import types, Dispatcher
from create_bot import dp, bot
from keyboards import kb_client 
from aiogram.types import ReplyKeyboardRemove
from data_base import sqlite_db

async def command_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Привет, игрок в 101! ', reply_markup = kb_client)
#        await message.delete()
    except:
        await message.reply('Общение с ботом через ЛС, напишите ему:\nhttps://t.me/Dlya101bot')


#async def chet_command(message: types.Message):
#    await bot.send_message(message.from_user.id, 'отжимания')

#async def otj_command(message: types.Message):
#    await bot.send_message(message.from_user.id, 'счет')

#@dp.message_handler(commands=["Данные"])
async def menu_command(message: types.Message):
    await sqlite_db.sql_read(message)

#async def menu_command1(message: types.Message):
#    await sqlite_db.sql_read1(message)

def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
#    dp.register_message_handler(chet_command, commands=['Отжимания'])
#    dp.register_message_handler(otj_command, commands=['Счет'])
    dp.register_message_handler(menu_command, commands=['Данные'])
#    dp.register_message_handler(menu_command1, commands=['Игроки'])
    