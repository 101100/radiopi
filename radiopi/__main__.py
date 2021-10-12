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

from radiopi import mixer, player, pollyannounce, rotary, streams # pylint: disable=wrong-import-position


# number of discreet volume steps
MIXER_STEPS = 20
# starting volume step
STARTING_VOLUME = 15

# the pin to enable or disable the amplifier
AMP_ENABLE_PIN = 4

# the pins for the rotary encoder (for volume)
ROTARY_PIN_1 = 23
ROTARY_PIN_2 = 24
# the pins for the play/stop button
BUTTON_PIN = 18


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



def enable_amp(enabled):
    """
    Enables the amplifier by setting the output pin appropriately.
    """
    GPIO.output(AMP_ENABLE_PIN, enabled)


def initialize_amp():
    """
    Sets up the amplifier output pin and initializes it to off.
    """
    GPIO.setup(AMP_ENABLE_PIN, GPIO.OUT)
    enable_amp(False)



def main():
    """
    The main method for the radiopi module.
    """
    initialize_amp()

    mix = mixer.Mixer(MIXER_STEPS)
    mix.set_value(STARTING_VOLUME)

    _rot = rotary.RotaryEncoder(ROTARY_PIN_1, ROTARY_PIN_2, mix.set_value, mix.get_value(), 0, MIXER_STEPS)

    streams_list = get_streams_list()
    play = player.RadioPlayer(announce, enable_amp, *streams_list)

    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    enable_amp(True)
    announce('Radio Pi Started')
    time.sleep(.5)

    if have_internet():
        announce('Internet connection found')
        # since we have a connection, get the speech file for the lack of connection while we can
        pollyannounce.get_speech_file('Internet connection not found')
    else:
        announce('Internet connection not found')

    enable_amp(False)
    time.sleep(.5)

    while True:
        sys.stdout.write('Waiting for press...')
        sys.stdout.flush()
        GPIO.wait_for_edge(BUTTON_PIN, GPIO.FALLING)
        print(' button pressed!')
        play.next_station()
        sys.stdout.write('Sleeping...')
        sys.stdout.flush()
        time.sleep(.4)
        print(' done.')



main()
