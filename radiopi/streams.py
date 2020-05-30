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
    def __init__(self, streams=None, streams_filename=None):
        if streams is not None:
            self.__all_streams = streams
        elif streams_filename is not None:
            self.__loadStreams(streams_filename)
        else:
            self.__loadStreams(DEFAULT_STREAMS_FILENAME)


    def __loadStreams(self, streams_filename):
        filename_with_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], streams_filename)
        try:
            with open(filename_with_path) as data_file:
                self.__allStreams = json.load(data_file)
        except:
            self.__allStreams = DEFAULT_STREAMS



    def getRandomStation(self):
        return random.sample(self.__allStreams.keys(), 1)[0]



    def getStream(self, station):
        return self.__allStreams[station]['stream']



    def getDescription(self, station):
        info = self.__allStreams[station]

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

        description = "{0}, {1} {2} from {3} {4}".format(station, info['band'], frequency, info['city'], info['state'])

        return description


if __name__ == '__main__':
    streams = StreamsHolder()
    randomStation = streams.getRandomStation()
    print 'Decsription', streams.getDescription(randomStation)
    print 'Stream', streams.getStream(randomStation)
