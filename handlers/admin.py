from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp, bot
from aiogram.dispatcher.filters import Text
from data_base import sqlite_db
from keyboards import admin_kb
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

ID = None

class FSMAdmin(StatesGroup):
    name = State()
    otj = State()
    chet = State()

class FSMred(StatesGroup):
    rname = State()
    rchet = State()
    rotj = State()

async def red_start(message: types.Message):
    if message.from_user.id == ID:  
        await FSMred.rname.set()
        await message.reply('Напиши имя')

async def red_name(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data: 
            data['name'] = message.text
        await FSMred.next()
        await message.reply('Введи счет')

async def red_chet(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data: 
            data['chet'] = float(message.text)
        await FSMred.next()
        await message.reply('Введи отжимания')

async def red_otj(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data: 
            data['otj'] = float(message.text)
        await sqlite_db.sql_red(state)
        await state.finish()
        await message.reply('Изменил')


async def admin_menu_command(message: types.Message):
    await sqlite_db.sql_read(message)

async def sql_obnul_command(message: types.Message):
    await sqlite_db.sql_read(message)

#@dp.message_handler(commands='god', is_chat_admin=True)
async def make_changes_command(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, "Привет, админ!", reply_markup=admin_kb.button_case_admin)
#    await message.delete()

#@dp.message_handler(commands='Загрузить', state = None)
async def cm_start(message: types.Message):
    if message.from_user.id == ID:  
        await FSMAdmin.name.set()
        await message.reply('Напиши имя')

async def cancel_handler(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await sqlite_db.state.finish(state)
        await message.reply('Ок')

#@dp.message_handler(state = FSMAdmin.name)
async def load_name(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data: 
            data['name'] = message.text
        await FSMAdmin.next()
        await message.reply('Напиши отжимания')

#@dp.message_handler(state = FSMAdmin.otj)
async def load_otj(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data: 
            data['otj'] = float(message.text)
        await FSMAdmin.next()
        await message.reply('Введи счет')

#@dp.message_handler(state = FSMAdmin.chet)
async def load_chet(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:    
        async with state.proxy() as data: 
            data['chet'] = float(message.text)
        await sqlite_db.sql_add_command(state)
        await state.finish()
        await message.reply('Добавил')

@dp.callback_query_handler(lambda x: x.data and x.data.startswith('del '))
async def del_callback_run(callback_query: types.CallbackQuery):
    await sqlite_db.sql_delete_command(callback_query.data.replace('del ', ''))
    await callback_query.answer(text=f'{callback_query.data.replace("del", "")} удален.', show_alert=True)

@dp.message_handler(commands='Удалить')
async def delete_item(message: types.Message):
    if message.from_user.id == ID:
        read = await sqlite_db.sql_read2()
        for ret in read:
            await bot.send_message(message.from_user.id, f'{ret[0]}\nАнжуманя: {ret[1]}\nСчет: {ret[2]}') 
            await bot.send_message(message.from_user.id, text = '^^^', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(f'Удалить {ret[0]}',callback_data=f'del {ret[0]}')))


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(cm_start, commands=['Загрузить'], state = None)
    dp.register_message_handler(load_name, state = FSMAdmin.name)
    dp.register_message_handler(load_otj, state = FSMAdmin.otj)
    dp.register_message_handler(load_chet, state = FSMAdmin.chet)
    dp.register_message_handler(make_changes_command, commands=['god'], is_chat_admin=True)
    dp.register_message_handler(cancel_handler, commands="cancel", state="*")
    dp.register_message_handler(cancel_handler, Text(equals="отмена", ignore_case=True), state="*")
    dp.register_message_handler(admin_menu_command, commands=['Данные'])
    dp.register_message_handler(sql_obnul_command, commands=['Обнулить'])
    dp.register_message_handler(red_start, commands=['Изменить'], state = None)
    dp.register_message_handler(red_name, state = FSMred.rname)
    dp.register_message_handler(red_chet, state = FSMred.rchet)
    dp.register_message_handler(red_otj, state = FSMred.rotj)
