# raspifon

Baby monitor via Raspberry Pi. If a noise like a baby scream is detected, the audio recording starts and sends a notification via Telegram.

To be able to use it, you must create a new Telegram bot.


## Installation

Install the following dependencies:

```
sudo apt-get install portaudio19-dev python-pyaudio python3-pyaudio ffmpeg
pip3 install PyAudio
pip3 install AudioSegment
pip3 install opencv-python
pip3 install python-telegram-bot
```

## Sound device

Check the audio device that shall be used for recording:

```
python3 check-audio-devices.py
```

And set the index to AudioDeviceIndex in settings.ini

To get rid of error messages caused by PyAudio, the following lines can be removed or commented out of /usr/share/alsa/alsa.conf:

```
# pcm.front cards.pcm.front
# pcm.rear cards.pcm.rear
# pcm.center_lfe cards.pcm.center_lfe
# pcm.side cards.pcm.side
# pcm.surround21 cards.pcm.surround21
# pcm.surround40 cards.pcm.surround40
# pcm.surround41 cards.pcm.surround41
# pcm.surround50 cards.pcm.surround50
# pcm.surround51 cards.pcm.surround51
# pcm.surround71 cards.pcm.surround71
```


## Telegram Bot

Please create your own Telegram Bot from @BotFather. You will receive a key that must be stored in the settings.ini

## Running the bot

Start the telegram bot

```
python3 raspifon.py
```

## Authorization

The raspifon can only be used by certain users. To be able to use it with your Telegram user, add your user id to the AllowedUsers in the settings.ini. When you start to chat with your bot, you will see your user id logged by the raspifon.

## Commands

| Command     | Description   |
| ----------- | ------------- |
| /watch      | start watch (ie audio recording and sending notifications) |
| /off        | stop watching |
| /pic        | take a picture |
