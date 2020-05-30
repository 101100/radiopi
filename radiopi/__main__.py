import os
import socket
import sys
import time

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

import rotary
import mixer
import player
import pollyannounce


# number of discreet volume steps
MIXER_STEPS = 20
# starting volume step
STARTING_VOLUME = 15

# the pins for the rotary encoder (for volume)
ROTARY_PIN_1 = 23
ROTARY_PIN_2 = 24
# the pins for the play/stop button
BUTTON_PIN = 18


def announce(announcement):
    # mirror announcement to screen
    sys.stdout.write(announcement + '\n')
    sys.stdout.flush()
    pollyannounce.play_speech(announcement)



def internet(host="8.8.8.8", port=53, timeout=3):
    """
    Host: 8.8.8.8 (google-public-dns-a.google.com)
    OpenPort: 53/tcp
    Service: domain (DNS/TCP)
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception as ex:
        return False



def main():
    mix = mixer.Mixer(MIXER_STEPS)
    mix.setValue(STARTING_VOLUME)

    rot = rotary.RotaryEncoder(ROTARY_PIN_1, ROTARY_PIN_2, mix.setValue, mix.getValue(), 0, MIXER_STEPS)

    play = player.RadioPlayer(announce)

    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    announce('Radio Pi Started')
    time.sleep(.5)

    if internet():
        announce('Internet connection found')
    else:
        announce('Internet connection not found')

    time.sleep(.5)

    while True:
        sys.stdout.write('Waiting for press...')
        sys.stdout.flush()
        GPIO.wait_for_edge(BUTTON_PIN, GPIO.FALLING)
        print ' button pressed!'
        play.nextStation()
        sys.stdout.write('Sleeping...')
        sys.stdout.flush()
        time.sleep(.4)
        print ' done.'



main()
