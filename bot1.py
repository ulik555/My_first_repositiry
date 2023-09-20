import config
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from telegram.ext import filters, MessageHandler
from pyowm.owm import OWM

TOKEN = config.TOKEN
KEY = config.KEY
owm = OWM(KEY)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


def get_weather(city):
    mgr = owm.weather_manager()
    weather = mgr.weather_at_place(city).weather
    temperature = weather.temperature('celsius')

    return f'Погода в {city}: Температура: {temperature} C'


async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # text = update.message.text
    # city = text  # .split(' ')[1]city
    weather = get_weather('Ростов-на-Дону')
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=weather)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="command start: I'm bot")


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = 'Есть команды: \n/start - запуск бота\n /help - покажет команды'
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=text)


async def message_and_echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    if text == 'hi':
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text='Hello amigo')
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=update.message.text)

if __name__ == '__main__':

    application = ApplicationBuilder().token(TOKEN).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    help_handler = CommandHandler('help', help)
    application.add_handler(help_handler)

    weather_handler = CommandHandler('wether', weather)
    application.add_handler(weather_handler)

    message_handler = MessageHandler((filters.TEXT), message_and_echo)
    application.add_handler(message_handler)

    application.run_polling()
