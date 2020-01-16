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

config = configparser.ConfigParser()
config.read('settings.ini')

recorder = None
snapshot = None

class Raspifon:
    bot = None
    allowed_users = []
    watching_users = []

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
        logger.info('Entering watch - %s', user['id'])

        # check user permissions
        if user['id'] in self.allowed_users:
            # check if user is already watching
            if user['id'] in self.watching_users:
                update.message.reply_text('already watching')
            else:
                # start new recorder if first user
                if len(self.watching_users) == 0:
                    self.recorder_thread = Thread(target = recorder.listen)
                    self.recorder_thread.start()

                self.watching_users.append(user['id'])
                update.message.reply_text('starting to watch')

        else:
            update.message.reply_text('you are not allowed to run this service')

        logger.info('currently watching users: %s', self.watching_users)


    # Callback when an audio is recorded
    def callback(self, stream):
        if len(self.watching_users) == 0:
            logger.info('no one watching')
        else:
            logger.info('sending voice message')

            for userId in self.watching_users:
                self.bot.send_voice(chat_id=userId, voice=stream)


    # Turn the watch handler off.
    def off(self, update, context):
        user = update.message.from_user
        logger.info('stop watching - %s', user['id'])

        if user['id'] in self.watching_users:
            self.watching_users.remove(user['id'])
            update.message.reply_text('stopped watching')

            if len(self.watching_users) == 0:
                logger.info('turning recorder off')
                update.message.reply_text('raspifon turned off')
                recorder.stop()
            else:
                logger.info('recorder still on')

                update.message.reply_text('raspifon turned off')
                update.message.reply_text('but raspifon is still running')

        else:
            update.message.reply_text('you have not been watching')


    def picture(self, update, context):
        user = update.message.from_user

        if user['id'] in self.allowed_users:
            stream = snapshot.takePicture()

            if stream is None:
                logger.error('could not get picture')
            else:
                self.bot.send_photo(chat_id=user['id'], photo=stream)

        else:
            update.message.reply_text('you are not allowed to run this service')


    def error(self, update, context):
        logger.warning('Update "%s" caused error "%s"', update, context.error)


    def startBot(self):
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
recorder = Recorder(raspifon, config['DEFAULT']['AudioDeviceIndex'])

# Create the snapshot
snapshot = Snapshot(config['DEFAULT']['CameraDeviceIndex'])

raspifon.startBot()
