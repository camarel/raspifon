import logging
import configparser
import json

from recorder import Recorder
from snapshot import Snapshot
from threading import Thread
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


# Enable logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
recorder = None
snapshot = None

class Raspifon:
    user_id = None
    bot = None
    allowed_users = []

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

        if user['id'] in self.allowed_users:
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


    def picture(self, update, context):
        if user['id'] in self.allowed_users:
            filename = snapshot.takePicture()

            if filename is None:
                logger.error('could not get filename')
            else:
                user = update.message.from_user
                self.bot.send_photo(chat_id=user['id'], photo=open(filename, 'rb'))
        else:
            update.message.reply_text('you are not allowed to run this service')


    def error(self, update, context):
        logger.warning('Update "%s" caused error "%s"', update, context.error)


    def startBot(self):
        config = configparser.ConfigParser()
        config.read('settings.ini')
        self.allowed_users = json.loads(config['DEFAULT']['AllowedUsers'])

        # Create the Updater
        updater = Updater(config['DEFAULT']['Token'], use_context=True)

        # Get the dispatcher to register handlers
        dp = updater.dispatcher

        # start with the bot command
        dp.add_handler(CommandHandler("start", self.start))

        # start audio watch
        dp.add_handler(CommandHandler("w", self.watch))
        dp.add_handler(CommandHandler("watch", self.watch))

        # stop audio watch
        dp.add_handler(CommandHandler("off", self.off))
        dp.add_handler(CommandHandler("stop", self.off))

        # take a picture
        dp.add_handler(CommandHandler("p", self.picture))
        dp.add_handler(CommandHandler("pic", self.picture))
        dp.add_handler(CommandHandler("picture", self.picture))

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

# Create the audio recorder
recorder = Recorder(raspifon)

snapshot = Snapshot()

raspifon.startBot()
