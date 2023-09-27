# импортируем функции: погоды и валюты, и токен бота
from config import get_weather, get_valute, TOKEN
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from telegram.ext import filters, MessageHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

from pyowm.commons.exceptions import NotFoundError


# настройки модуля ведения журнала
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
# кнопки клавиатуры
reply_keyboard = [['/kurs', '/help'],
                  ['/weather', 'close']]

markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # кнопка старт выводит приветствие и описание бота и клавиатуру
    await update.message.reply_text(
        """\t\t\tПривет!\n я бот который покажет прогноз погоды
и курс валют\n\n\t\t\tВведите название города""", reply_markup=markup)


async def close_keyboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Закрывает клавиатуру
    update.message.reply_text('Ok', reply_markup=ReplyKeyboardRemove())


async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Введите город, чтобы узнать погоду')
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=message_client(update, context))


async def exchange_rate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # при нажатии на кнопку kurs  выведет курс валюты
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=get_valute())


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = '''Есть команды: \n/start - запуск бота\n/kurs - выведет курс валют
/help - покажет команды\n/weather - покажет прогноз погоды'''
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=text)


async def message_client(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    if text == 'close':
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text='клавиатура закрыта')
    else:
        try:
            city = update.message.text
            weather = get_weather(city)
            await context.bot.send_message(
                chat_id=update.effective_chat.id, text=weather)
        except NotFoundError:
            await update.message.reply_text(
                'Вы ввели не коректно название города!!!\nПовторите ввод!')


if __name__ == '__main__':

    application = ApplicationBuilder().token(TOKEN).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    valute_handler = CommandHandler('kurs', exchange_rate)
    application.add_handler(valute_handler)

    weather_handler = CommandHandler('weather', weather)
    application.add_handler(weather_handler)

    help_handler = CommandHandler('help', help)
    application.add_handler(help_handler)

    close_handler = CommandHandler('close', close_keyboard)
    application.add_handler(close_handler)

    message_handler = MessageHandler((filters.TEXT), message_client)
    application.add_handler(message_handler)

    application.run_polling()


#