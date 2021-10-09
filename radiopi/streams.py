"""
Includes methods for collecting a set of internet radio streams.
"""

import json
import os
import random
import re


DEFAULT_STREAMS = \
  { 'CHQR':   { 'band': 'AM',
                'city': 'Calgary',
                'freq': '770',
                'letters': 'CHQR',
                'state': 'Alberta',
                'stream': 'http://live.leanstream.co/CHQRAM?type=.aac' },
    'KBUL':   { 'band': 'AM',
                'city': 'Billings',
                'freq': '970',
                'letters': 'KBUL',
                'state': 'Montana',
                'stream': 'http://playerservices.streamtheworld.com/pls/KBULFMAAC.pls' },
    'KFYR':   { 'band': 'AM',
                'city': 'Bismarck',
                'freq': '550',
                'letters': 'KFYR',
                'state': 'North Dakota',
                'stream': 'http://kfyr-am.akacast.akamaistream.net/7/536/26911/v1/auth.akacast.akamaistream.net/kfyr-am' } }

DEFAULT_STREAMS_FILENAME = 'streams.json'


class StreamsHolder:
    """
    Holds a set of internet radio streams along with enough attributes to
    describe each stream.
    """
    def __init__(self, streams_list=None, streams_filename=None):
        if streams_list is not None:
            self.__all_streams = streams_list
        elif streams_filename is not None:
            self.__load_streams(streams_filename)
        else:
            self.__load_streams(DEFAULT_STREAMS_FILENAME)


    def __load_streams(self, streams_filename):
        if os.path.isabs(streams_filename):
            filename_with_path = streams_filename
        else:
            filename_with_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], streams_filename)
        try:
            with open(filename_with_path) as data_file: # pylint: disable=unspecified-encoding
                self.__all_streams = json.load(data_file)
        except: # pylint: disable=bare-except
            self.__all_streams = DEFAULT_STREAMS



    def get_random_station(self):
        """
        Returns a random station from the streams list.
        """
        return random.sample(self.__all_streams.keys(), 1)[0]



    def get_stream(self, station):
        """
        Retrieves the given station by its key.
        """
        return self.__all_streams[station]['stream']



    def get_description(self, station):
        """
        Computes the description for the given station. The description is
        tweaked to make it sound like a human might say it when passed to a
        text-to-speach algorithms.
        """
        info = self.__all_streams[station]

        if 'description' in info.keys():
            return info['description']

        station = re.sub(r"(?<=\w)(\w)", r" \1", station)
        station = station.replace('A', 'Eh')
        frequency = info['freq']
        if info['band'] == 'AM':
            frequency = re.sub(r"(\d\d)$", r" \1", frequency)
            frequency = frequency.replace('00', 'hundred')
        else:
            frequency = frequency.replace('00', ' hundred ')
            frequency = re.sub(r"(?<=\d)(\d)(\d)", r" \1 \2", frequency)
            frequency = frequency.replace('0', 'Oh')
            frequency = frequency.replace('.', ' point ')

        description = f"{station}, {info['band']} {frequency} from {info['city']} {info['state']}"

        return description


if __name__ == '__main__':
    streams = StreamsHolder()
    randomStation = streams.get_random_station()
    print('Decsription', streams.get_description(randomStation))
    print('Stream', streams.get_stream(randomStation))
