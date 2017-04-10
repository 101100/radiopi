import os
import sys
import time

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

import rotary
import mixer
import player
import pollyannounce


STARTING_VOLUME = 13
MIXER_STEPS = 20
BUTTON_CHANNEL = 18


def announce(announcement):
    # mirror announcement to screen
    sys.stdout.write(announcement + '\n')
    sys.stdout.flush()
    pollyannounce.play_speech(announcement)



def main():
    mix = mixer.Mixer(MIXER_STEPS)
    mix.setValue(13)

    rot = rotary.RotaryEncoder(23, 24, mix.setValue, mix.getValue(), 0, MIXER_STEPS)

    play = player.RadioPlayer(announce)

    GPIO.setup(BUTTON_CHANNEL, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    announce('Radio Pi Started')
    time.sleep(.5)

    while True:
        sys.stdout.write('Waiting for press...')
        sys.stdout.flush()
        GPIO.wait_for_edge(BUTTON_CHANNEL, GPIO.FALLING)
        print ' button pressed!'
        play.nextStation()
        sys.stdout.write('Sleeping...')
        sys.stdout.flush()
        time.sleep(.4)
        print ' done.'



main()
