# raspifon

This is a baby monitor via Raspberry Pi.


## Installation

Install the following dependencies:

```
sudo apt-get install portaudio19-dev python-pyaudio python3-pyaudio
sudo pip3 install PyAudio
sudo pip3 install AudioSegment
```

Create the directory where the audio files will be stored:

```
mkdir records
```

## Sound device

Check the audio device that shall be used

```
python3 check-audio-devices.py
```

And set the 'dev_index' in recorder.py

## Running the bot

Start the telegram bot

```
python3 raspifon.py
```
