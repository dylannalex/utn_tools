import telegram
from telegram.ext import Filters
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from utn_tools.tgm import settings
from utn_tools.tgm import commands

if settings.MODE == "test":
    # Local access
    def run(updater):
        updater.start_polling()
        print("[STATUS] bot loaded")
        updater.idle()  # End bot with ctrl + C


elif settings.MODE == "deploy":
    # Heroku access
    def run(updater):
        updater.start_webhook(
            listen="0.0.0.0", port=settings.PORT, url_path=settings.TOKEN
        )
        updater.bot.set_webhook(
            f"https://{settings.HEROKU_APP_NAME}.herokuapp.com/{settings.TOKEN}"
        )


def main() -> None:
    bot = telegram.Bot(token=settings.TOKEN)
    updater = Updater(bot.token, use_context=True)
    dp = updater.dispatcher

    # Commands
    dp.add_handler(CommandHandler("start", commands.help))
    dp.add_handler(CommandHandler("help", commands.help))
    dp.add_handler(MessageHandler(Filters.text, commands.parser))
    run(updater)


if __name__ == "__main__":
    main()
