import os
import subprocess
import threading
import shutil
import signal
import time
import tempfile
from datetime import datetime
from datetime import timedelta

from mpd import MPDClient


class RadioPlayer:
    def __init__(self, announce, *args):
        self.announce = announce
        self.currentStationName = None
        self.playCount = 0
        self.streamsList = args
        self.nextStreams = 0
        self.lock = threading.Lock()
        self.mpdClient = MPDClient()
        self.mpdClient.connect("localhost", 6600)
        self.mpdClient.repeat(1)
        self.mpdClient.stop()
        self.mpdClient.clear()
        self.mpdClient.disconnect()


    def nextStation(self):
        if self.playCount < 1:
            self.playStation(self.streamsList[self.nextStreams])
            self.playCount += 1
            self.nextStreams = (self.nextStreams + 1) % len(self.streamsList)
        else:
            self.stopPlaying()
            self.playCount = 0


    def playStation(self, streams):
        stationName = streams.getRandomStation()
        self.playUrl(streams.getStream(stationName), streams.getDescription(stationName))


    def playUrl(self, url, description):
        self.lock.acquire()
        try:
            if self.currentStationName is not None:
                self.__stop__()

            self.mpdClient.connect("localhost", 6600)
            self.mpdClient.add(url)

            time.sleep(0.2)
            self.announce(description)

            self.mpdClient.play()
            self.mpdClient.disconnect()

            self.currentStationName = description
        finally:
            self.lock.release()


    def stopPlaying(self):
        self.lock.acquire()
        try:
            self.__stop__()
            time.sleep(0.2)
            self.announce("Stopped")
        finally:
            self.lock.release()


    def __stop__(self):
        self.mpdClient.connect("localhost", 6600)
        self.mpdClient.stop()
        self.mpdClient.clear()
        self.mpdClient.disconnect()
        self.currentStationName = None
        self.playCount = 0
