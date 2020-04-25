from geocoder import get_ll_span
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests
import json


def start(update, context):
    update.message.reply_text("Я бот-геокодер. Ищу объекты на карте.")


def geocoder(update, context):
    try:
        ll, spn = get_ll_span(update.message.text)
        if ll and spn:
            point = "{ll},pm2vvl".format(ll=ll)
            static_api_request = "http://static-maps.yandex.ru/1.x/?ll={ll}&spn={spn}&l=map&pt={point}".format(
                **locals())
            context.bot.sendPhoto(update.message.chat.id, static_api_request, caption=update.message.text)
        else:
            update.message.reply_text("По запросу ничего не найдено.")
    except RuntimeError as ex:
        update.message.reply_text(str(ex))


def main():
    updater = Updater("YOUR_TOKEN", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text, geocoder))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()