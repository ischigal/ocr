import telegram
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from subprocess import call
import threading

def refreshmenue():
	call(["python","lunchprinter.py"])
	threading.Timer(600, refreshmenue).start()

refreshmenue()

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
	"""Send a message when the command /start is issued."""
	update.message.reply_text('Hi!')

def help(update, context):
	"""Send a message when the command /help is issued."""
	update.message.reply_text('Use:\n /today for today\'s lunch \n /tomorrow for tomorrow\'s lunch \n /week for the entire week menue')

def today(update, context):

	file_today = open("today_out.txt","r")
	menue_today = file_today.read()
	file_today.close()
	update.message.reply_text(menue_today, parse_mode=telegram.ParseMode.MARKDOWN)
	#pictoday = open('today_out.png', 'rb')
	#update.message.reply_photo(photo=pictoday)
	#pictoday.close()

def tomorrow(update, context):

	file_tomorrow = open("tomorrow_out.txt","r")
	menue_tomorrow = file_tomorrow.read()
	file_tomorrow.close()
	update.message.reply_text(menue_tomorrow, parse_mode=telegram.ParseMode.MARKDOWN)
	#pictomorrow = open('tomorrow_out.png', 'rb')
	#update.message.reply_photo(photo=pictomorrow)
	#pictomorrow.close()



def week(update, context):
	
	file_week = open("week_out.txt","r")
	menue_week = file_week.read()
	file_week.close()
	if len(menue_week) > 4000:
		update.message.reply_text(menue_week[:len(menue_week)//2],parse_mode=telegram.ParseMode.MARKDOWN)
		update.message.reply_text(menue_week[len(menue_week)//2:],parse_mode=telegram.ParseMode.MARKDOWN)
	else:
		update.message.reply_text(menue_week, parse_mode=telegram.ParseMode.MARKDOWN)
	#picweek = open('week_out.png', 'rb')
	#update.message.reply_photo(photo=picweek)
	#picweek.close()


def error(update, context):
	"""Log Errors caused by Updates."""
	logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
	"""Start the bot."""
	# Create the Updater and pass it your bot's token.
	# Make sure to set use_context=True to use the new context based callbacks
	# Post version 12 this will no longer be necessary
	updater = Updater("795034477:AAEm7BKRleIuIwRM9Jdj2asL_5_vo3Y3AkU", use_context=True)

	# Get the dispatcher to register handlers
	dp = updater.dispatcher

	# on different commands - answer in Telegram
	dp.add_handler(CommandHandler("start", start))
	dp.add_handler(CommandHandler("help", help))
	dp.add_handler(CommandHandler("today", today))
	dp.add_handler(CommandHandler("tomorrow", tomorrow))
	dp.add_handler(CommandHandler("week", week))

	# on noncommand - send help info:
	dp.add_handler(MessageHandler(Filters.text, help))

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