import asyncio
import datetime
import config
import pytz
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils import exceptions


bot = Bot(token=config.bot_token)
dispatcher = Dispatcher(bot)

# Dictionary with names and birthdays
birthday_dict = {
    'user1': datetime.date(2001, 1, 10),
    'user2': datetime.date(2002, 2, 15),
    'user3': datetime.date(2003, 3, 20),
    'user4': datetime.date(2004, 4, 25),
    'user5': datetime.date(2005, 5, 30)
}


feasts_dict = {
    'дівчат з 8 березня!🥰🌹': datetime.date(2000, 3, 8),
    'з Новим роком🎁🎉🎊': datetime.date(2000, 1, 1)
}


@dispatcher.message_handler(commands=['start'])
async def start(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text="Привіт! Я Birthbot. Я буду нагадувати Вам про дні народження ваших друзів!")

timezone = pytz.timezone('Europe/Kyiv')


async def check_birthday():
    today = datetime.date.today()
    for name, birthday in birthday_dict.items():
        age = today.year - birthday.year
        if birthday.day == today.day and birthday.month == today.month:
            if age == 17 or age == 18 or age == 19 or age == 20 or age == 25 or age == 26 or age == 27 or age == 28 or age == 29 or age == 30:
                message = f"🥳Сьогодні {name} виповнилось {age} років, з днем народження! 🎉🎂🎁"
            elif age == 21:
                message = f"🥳Сьогодні {name} виповнилось {age} рік, з днем народження! 🎉🎂🎁"
            else:
                message = f"🥳Сьогодні {name} виповнилось {age} роки, з днем народження! 🎉🎂🎁"
            try:
                await bot.send_message(chat_id=config.chat_id, text=message)
            except exceptions.BotBlocked:
                print(f"Target [ID:{config.chat_id}]: blocked by user")
            except exceptions.ChatNotFound:
                print(f"Target [ID:{config.chat_id}]: invalid chat ID")
    for fest, date in feasts_dict.items():
        if date.day == today.day and date.month == today.month:
            message2 = f"🥳Вітаю {fest}"
            try:
                await bot.send_message(chat_id=config.chat_id, text=message2)
            except exceptions.BotBlocked:
                print(f"Target [ID:{config.chat_id}]: blocked by user")
            except exceptions.ChatNotFound:
                print(f"Target [ID:{config.chat_id}]: invalid chat ID")


# Function to check for birthdays
@dispatcher.message_handler(commands=['birthdays'])
async def send_birthdays(message: types.Message):
    today = datetime.date.today()
    month_birthdays = [(name, birthday.strftime("%d.%m.%Y")) for name,
                       birthday in birthday_dict.items() if birthday.month == today.month]
    if month_birthdays:
        reply_message = "Іменинники в цьому місяці:\n\n"
        for name, birthday in month_birthdays:
            reply_message += f"{name} ({birthday})\n"
    else:
        reply_message = "Цього місяця немає іменинників."
    await bot.send_message(chat_id=message.chat.id, text=reply_message)


async def scheduler():
    while True:
        await asyncio.sleep(60)
        now = datetime.datetime.now(timezone)
        if now.hour == 3 and now.minute == 0:
            await check_birthday()
        print(now)


async def main():
    # Start the scheduler
    await scheduler()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    executor.start_polling(dispatcher, loop=loop, skip_updates=True)


