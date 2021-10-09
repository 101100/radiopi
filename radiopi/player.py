"""
Defines methods for playing internet radio streams.
"""

import threading
import time

from mpd import MPDClient


class RadioPlayer:
    """
    Defines a player of internet radio streams that will ensure only one is
    playing at a time and will also enable an amplifier while it is playing
    and announce each station change.
    """
    def __init__(self, announce, enable_amp, *args):
        self.__announce = announce
        self.__enable_amp = enable_amp
        self.__current_station_name = None
        self.__play_count = 0
        self.__streams_list = args
        self.__next_streams = 0
        self.__lock = threading.Lock()
        self.__mpd_client = MPDClient()
        self.__mpd_client.connect("localhost", 6600)
        self.__mpd_client.repeat(1)
        self.__mpd_client.stop()
        self.__mpd_client.clear()
        self.__mpd_client.disconnect()


    def next_station(self):
        """
        Handles the "next station" action, which will either play a random
        stream or stop playing if it is playing.
        """
        if self.__play_count < 1:
            self.play_station(self.__streams_list[self.__next_streams])
            self.__play_count += 1
            self.__next_streams = (self.__next_streams + 1) % len(self.__streams_list)
        else:
            self.stop_playing()
            self.__play_count = 0


    def play_station(self, streams):
        """
        Plays a random station from the given set of streams.
        """
        station_name = streams.get_random_station()
        self.play_url(streams.get_stream(station_name), streams.get_description(station_name))


    def play_url(self, url, description):
        """
        Plays the given URL, announcing it using the given desription first.
        """
        with self.__lock:
            if self.__current_station_name is not None:
                self.__stop__()

            self.__enable_amp(True)
            self.__mpd_client.connect("localhost", 6600)
            self.__mpd_client.add(url)

            time.sleep(0.2)
            self.__announce(description)

            self.__mpd_client.play()
            self.__mpd_client.disconnect()

            self.__current_station_name = description


    def stop_playing(self):
        """
        Stops playing any streams, announces "stopped" and turns off the
        amplifier.
        """
        with self.__lock:
            self.__stop__()
            time.sleep(0.2)
            self.__announce("Stopped")
            self.__enable_amp(False)


    def __stop__(self):
        self.__mpd_client.connect("localhost", 6600)
        self.__mpd_client.stop()
        self.__mpd_client.clear()
        self.__mpd_client.disconnect()
        self.__current_station_name = None
        self.__play_count = 0
