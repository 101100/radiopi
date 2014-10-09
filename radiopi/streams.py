import random
import re


ALL_STREAMS = \
  { 'CHQR':   { 'band': 'AM',
                'city': 'Calgary',
                'freq': '770',
                'letters': 'CHQR',
                'state': 'Alberta',
                'stream': 'http://host1.leanstream-hd.com/CHQRAM?type=.aac' },
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



if __name__ == '__main__':
    randomStation = getRandomStation()
    randomStation = 'CJOB'
    print 'Decsription', getDescription(randomStation)
    print 'Stream', getStream(randomStation)
