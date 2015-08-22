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

ALL_STREAMS = {}

STREAMS_FILENAME = 'streams.json'


def __loadStreams():
    filename_with_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], STREAMS_FILENAME)
    try:
        with open(filename_with_path) as data_file:
            allStreams = json.load(data_file)
    except:
        allStreams = DEFAULT_STREAMS

    return allStreams



def getRandomStation():
    return random.sample(ALL_STREAMS.keys(), 1)[0]



def getStream(station='CHQR'):
    return ALL_STREAMS[station]['stream']



def getDescription(station='CHQR'):
    info = ALL_STREAMS[station]

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


ALL_STREAMS = __loadStreams()


if __name__ == '__main__':
    randomStation = getRandomStation()
    randomStation = 'CJOB'
    print 'Decsription', getDescription(randomStation)
    print 'Stream', getStream(randomStation)
