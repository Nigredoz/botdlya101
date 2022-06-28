import sqlite3 as sq
from create_bot import dp, bot

def sql_start():
	global base, cur
	base = sq.connect('telegram.bd')
	cur = base.cursor()
	if base:
		print('Data base connected OK!')
	base.execute('CREATE TABLE IF NOT EXISTS sostav(name TEXT PRIMARY KEY, otj INTEGER , chet INTEGER)')
	base.commit()

async def sql_add_command(state):
	async with state.proxy() as data:
		cur.execute('INSERT INTO sostav VALUES (?, ?, ?)', tuple(data.values()))
		base.commit()

async def sql_red(state):
	async with state.proxy() as data:
		cur.execute('UPDATE sostav SET chet = ? WHERE name = ''', tuple(data.values()))
		base.commit()

async def sql_read(message):
	for ret in cur.execute('SELECT * From sostav').fetchall():
		await bot.send_message(message.from_user.id, f'{ret[0]}\nАнжуманя: {ret[1]}\nСчет: {ret[2]}')

async def sql_read1(message):
	for ret in cur.execute('SELECT * From sostav').fetchall():
		await bot.send_message(message.from_user.id, f'Игроки:\n{ret[0]}')

async def sql_read2():
	return cur.execute('SELECT * FROM sostav').fetchall()

async def sql_delete_command(data):
	cur.execute('DELETE FROM sostav WHERE name == ?', (data,))
	base.commit()