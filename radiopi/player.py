import os
import subprocess
import threading
import shutil
import signal
import time
import tempfile
from datetime import datetime
from datetime import timedelta

from espeak import espeak
from mpd import MPDClient

import streams


class RadioPlayer:
    def __init__(self):
        self.currentStationName = None
        self.playCount = 0
        self.lock = threading.Lock()
        self.mpdClient = MPDClient()
        self.mpdClient.connect("localhost", 6600)
        self.mpdClient.stop()
        self.mpdClient.clear()


    def nextStation(self):
        if self.playCount < 1:
            self.playStation(streams.getRandomStation())
            self.playCount += 1
        else:
            self.stopPlaying()
            self.playCount = 0


    def playStation(self, stationName):
        self.lock.acquire()
        try:
            if self.currentStationName is not None:
                self.__stop__()

            self.mpdClient.add(streams.getStream(stationName))

            time.sleep(0.2)
            espeak.synth(streams.getDescription(stationName))
            while espeak.is_playing():
                time.sleep(0.2)

            self.mpdClient.play()

            self.currentStationName = stationName
        finally:
            self.lock.release()


    def stopPlaying(self):
        self.lock.acquire()
        try:
            self.__stop__()
            time.sleep(0.2)
            espeak.synth("Stopped")
        finally:
            self.lock.release()


    def __stop__(self):
        self.mpdClient.stop()
        self.mpdClient.clear()
        self.currentStationName = None

