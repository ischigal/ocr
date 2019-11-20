import telegram  # make sure that python-telegram-bot 12 or newer is installed
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import threading
import datetime

import lunchprinter

key = open("botkey.txt").readlines()[0].strip()
DEVID = int(open("botkey.txt").readlines()[1].strip())


def refreshmenue():   # TODO rework this function using import lunchprinter or something
    lunchprinter.lunchPrinter()
    print("last update", datetime.datetime.now())
    threading.Timer(3600, refreshmenue).start()


refreshmenue()

# Enable logging #TODO how does this work and what does it do?
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.


def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')
    update.message.reply_text('Use:\n /today for today\'s lunch \n /tomorrow for tomorrow\'s lunch \n /week for the entire week menue')  # immidiately show options


def help(update, context):
    """Send a message when the command /help is issued."""

    update.message.reply_text('Use:\n /today for today\'s lunch \n /tomorrow for tomorrow\'s lunch \n /week for the entire week menue')


def DEV_INFO(update, day):
    user_ID = update.message.from_user['id']
    if user_ID == DEVID:
        file_dev_flags = open("dev_flags_"+day+"_out.txt", "r")
        dev_flags = file_dev_flags.read()
        file_dev_flags.close()
        update.message.reply_text(dev_flags, parse_mode=telegram.ParseMode.MARKDOWN)


def today(update, context):

    DEV_INFO(update, "today")
    file_today = open("today_out.txt", "r")
    menue_today = file_today.read()
    file_today.close()
    update.message.reply_text(menue_today, parse_mode=telegram.ParseMode.MARKDOWN)


def tomorrow(update, context):

    DEV_INFO(update, "tomorrow")
    file_tomorrow = open("tomorrow_out.txt", "r")
    menue_tomorrow = file_tomorrow.read()
    file_tomorrow.close()
    update.message.reply_text(menue_tomorrow, parse_mode=telegram.ParseMode.MARKDOWN)


def week(update, context):

    DEV_INFO(update, "week")
    file_week = open("week_out.txt", "r")
    menue_week = file_week.read()
    file_week.close()
    if len(menue_week) > 4000:  # message character limit is around 4000 (4096 probably)
        update.message.reply_text(menue_week[:len(menue_week)//2], parse_mode=telegram.ParseMode.MARKDOWN)
        update.message.reply_text(menue_week[len(menue_week)//2:], parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        update.message.reply_text(menue_week, parse_mode=telegram.ParseMode.MARKDOWN)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)
    # TODO find out how this works


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(key, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("today", today))
    dp.add_handler(CommandHandler("tomorrow", tomorrow))
    dp.add_handler(CommandHandler("week", week))

    # on noncommand - send help info:
    dp.add_handler(MessageHandler(Filters.text, help))  # does not trigger on typos in commands e.g. /tomorow

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
