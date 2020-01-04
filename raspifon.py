import logging

from recorder import Recorder
from threading import Thread
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

allowed_users = [
    10203040,
    ]

# Enable logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
recorder = None

class Raspifon:
    user_id = None
    bot = None

    # Start handler to open new convertion with the bot.
    def start(self, update, context):
        user = update.message.from_user
        logger.info('Starting to talk with user %s, ID: %s',
                user['username'],
                user['id'])

        update.message.reply_text('Hi {}, welcome on blaui Tünta'.
                format(user['first_name']))


    # Handler to start watching and recording audio.
    def watch(self, update, context):
        user = update.message.from_user

        logger.info('Entering watch "%s"', user['id'])

        if user['id'] in allowed_users:
            if self.user_id is None:
                update.message.reply_text('starting to watch')

                thread = Thread(target = recorder.listen)
                thread.start()

                self.user_id = user['id']
            else:
                update.message.reply_text('already watching dude')
        else:
            update.message.reply_text('you are not allowed to run this service')


    # Callback when an audio is recorded
    def callback(self, filename):
        if self.user_id is None:
            logger.info('no one watching')
        else:
            logger.info('sending voice message "%s"', filename)
            self.bot.send_voice(chat_id=self.user_id, voice=open(filename, 'rb'))


    # Turn the watch handler off.
    def off(self, update, context):
        if self.user_id is None:
            update.message.reply_text('nothing running')
        else:
            self.user_id = None
            update.message.reply_text('stopped watching')
            recorder.stop()


    def error(self, update, context):
        logger.warning('Update "%s" caused error "%s"', update, context.error)


    def startBot(self):
        # Create the Updater
        updater = Updater("0000:APITOKEN-000", use_context=True)

        # Get the dispatcher to register handlers
        dp = updater.dispatcher

        # on different commands - answer in Telegram
        dp.add_handler(CommandHandler("start", self.start))
        dp.add_handler(CommandHandler("watch", self.watch))
        dp.add_handler(CommandHandler("off", self.off))

        self.bot = dp.bot

        # log all errors
        dp.add_error_handler(self.error)
        logger.info('up and running')

        # Start the Bot
        updater.start_polling()

        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        updater.idle()

# Create the telegram bot
raspifon = Raspifon()

# Create the recorder
recorder = Recorder(raspifon)

raspifon.startBot()