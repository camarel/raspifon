# This file is inspired by
# https://stackoverflow.com/questions/18406570/python-record-audio-on-detected-sound

import pyaudio
import math
import struct
import wave
import time
import os

from pydub import AudioSegment


class Recorder:
    # audio settings
    dev_index = 2    # device index found by p.get_device_info_by_index(ii)
    chunk     = 1024  # record in chunks of 1024 samples
    channels  = 1     # number of audio channels
    rate      = 16000 # record at 16000 frames per second
    sf        = pyaudio.paInt16 # 16 bits per sample

    # auto record settings
    directory = r'./records' # directory to save the files
    threshold = 80 # volume threshold to start recording
    timeout   = 3  # seconds to wait after last threshold

    # rms settings
    swidth = 2
    short_normalize = (1.0/32768.0)

    @staticmethod
    def rms(frame):
        count = len(frame) / Recorder.swidth
        format = '%dh' % (count)
        shorts = struct.unpack(format, frame)

        sum_squares = 0.0
        for sample in shorts:
            n = sample * Recorder.short_normalize
            sum_squares += n * n
        rms = math.pow(sum_squares / count, 0.5)

        return rms * 1000


    def __init__(self, bot):
        self.bot = bot


    def record(self):
        print('Noise detected, recording beginning')
        rec = []
        current = time.time()
        end = time.time() + self.timeout

        while current <= end:
            data = self.stream.read(self.chunk, exception_on_overflow = False)
            if self.rms(data) >= self.threshold: end = time.time() + self.timeout

            current = time.time()
            rec.append(data)
        self.write(b''.join(rec))


    def write(self, recording):
        if os.path.exists(self.directory):
            n_files = len(os.listdir(self.directory))
            file_wav = os.path.join(self.directory, '{}.wav'.format(n_files))
            file_mp3 = os.path.join(self.directory, '{}.mp3'.format(n_files))

            # creating wave file
            wf = wave.open(file_wav, 'wb')
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.p.get_sample_size(self.sf))
            wf.setframerate(self.rate)
            wf.writeframes(recording)
            wf.close()
            print('Written to file: {}'.format(file_wav))

            # converting to mp3
            sound = AudioSegment.from_wav(file_wav)
            sound.export(file_mp3, format='mp3')
            print('Converted to : {}'.format(file_mp3))

            # remove wav file
            os.remove(file_wav)

            self.bot.callback(file_mp3)
            print('Returning to listening')
        else:
            print('please create directory to write audio: {}'.format(self.directory))


    def listen(self):
        print('Listening beginning')
        self.listening = True
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.sf,
                                  channels=self.channels,
                                  rate=self.rate,
                                  input_device_index = self.dev_index,
                                  input=True,
                                  frames_per_buffer=self.chunk)

        while self.listening:
            input = self.stream.read(self.chunk, exception_on_overflow = False)
            rms_val = self.rms(input)
            if rms_val > self.threshold:
                self.record()

        print('Stop listening')
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

    def stop(self):
        self.listening = False

