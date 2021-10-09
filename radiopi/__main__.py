"""
Main method for radiopi module.
"""

import glob
import os
import socket
import sys
import time

from RPi import GPIO
GPIO.setmode(GPIO.BCM)

from radiopi import mixer, player, pollyannounce, streams # pylint: disable=wrong-import-position


# number of discreet volume steps
MIXER_STEPS = 20
# starting volume step
STARTING_VOLUME = 15

# Pirate Audio Pins
A_PIN = 5
B_PIN = 6
X_PIN = 16
Y_PIN = 24

# the pins for volume
VOLUME_UP_PIN = X_PIN
VOLUME_DOWN_PIN = Y_PIN
# the pins for the play/stop button
PLAY_PIN = A_PIN
SKIP_PIN = B_PIN


def announce(announcement):
    """
    An announcement method that will both speak and print the given text.
    """
    sys.stdout.write(announcement + '\n')
    sys.stdout.flush()
    pollyannounce.play_speech(announcement)



def have_internet(host="8.8.8.8", port=53, timeout=3):
    """
    Determines if the computer is connected to the internet by attempting to
    connect to the Google DNS server at:

    Host: 8.8.8.8 (google-public-dns-a.google.com)
    OpenPort: 53/tcp
    Service: domain (DNS/TCP)
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except: # pylint: disable=bare-except
        return False



def get_streams_list():
    """
    Attempts to read any configured streams from the filesystem and return
    them, falling back to a minimal default set.
    """
    streams_list = []

    for file in glob.glob(os.path.join(os.path.split(os.path.realpath(__file__))[0], "streams*.json")):
        print("Reading streams from file: '" + file + "'")
        streams_list.append(streams.StreamsHolder(streams_filename=file))

    if len(streams_list) == 0:
        print("No streams files found, using default streams list...")
        streams_list.append(streams.StreamsHolder())

    return streams_list



def main():
    """
    The main method for the radiopi module.
    """
    mix = mixer.Mixer(MIXER_STEPS)
    mix.set_value(STARTING_VOLUME)

    GPIO.setup(VOLUME_UP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(VOLUME_DOWN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(VOLUME_UP_PIN, GPIO.FALLING, callback=lambda _: mix.turn_up(), bouncetime=200)
    GPIO.add_event_detect(VOLUME_DOWN_PIN, GPIO.FALLING, callback=lambda _: mix.turn_down(), bouncetime=200)

    streams_list = get_streams_list()
    play = player.RadioPlayer(announce, (lambda _: None), *streams_list)

    GPIO.setup(PLAY_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(SKIP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    announce('Radio Pi Started')
    time.sleep(.5)

    if have_internet():
        announce('Internet connection found')
        # since we have a connection, get the speech file for the lack of connection while we can
        pollyannounce.get_speech_file('Internet connection not found')
    else:
        announce('Internet connection not found')

    GPIO.add_event_detect(PLAY_PIN, GPIO.FALLING)
    GPIO.add_event_detect(SKIP_PIN, GPIO.FALLING)
    sys.stdout.write('Waiting for press...')
    sys.stdout.flush()

    while True:
        if GPIO.event_detected(PLAY_PIN) or GPIO.event_detected(SKIP_PIN):
            print(' button pressed!')
            play.next_station()
            sys.stdout.write('Sleeping...')
            sys.stdout.flush()
            time.sleep(.4)
            print(' done.')
            sys.stdout.write('Waiting for press...')
            sys.stdout.flush()
            # read from both to clear their flags (I hope)
            GPIO.event_detected(PLAY_PIN)
            GPIO.event_detected(SKIP_PIN)
        else:
            time.sleep(.1)


main()
