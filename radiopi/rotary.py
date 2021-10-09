"""
Includes methods for dealing with a rotary encoder.
"""

import math
import time

from RPi import GPIO


STEPS_PER_TICK = 4


class RotaryEncoder:
    """
    Handles decoding a rotary encoder and keeping track of the relative
    changes in a numeric value.
    """
    #----------------------------------------------------------------------
    # Pass the wiring pin numbers here.  See:
    #  https://projects.drogon.net/raspberry-pi/wiringpi/pins/
    #----------------------------------------------------------------------
    def __init__(self, a_pin, b_pin, callback, startValue=0, minValue=0, maxValue=100):
        self.__a_pin = a_pin
        self.__b_pin = b_pin
        self.__update_callback = callback
        self.__min_raw_value = minValue * STEPS_PER_TICK
        self.__max_raw_value = maxValue * STEPS_PER_TICK

        GPIO.setup(a_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(b_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        self.__raw_value = startValue * STEPS_PER_TICK
        self.__last_delta = 0
        self.__r_seq = self.rotation_sequence()

        GPIO.add_event_detect(a_pin, GPIO.BOTH, callback=self.update)
        GPIO.add_event_detect(b_pin, GPIO.BOTH, callback=self.update)


    def rotation_sequence(self):
        """
        Returns the quadrature encoder state converted into
        a numerical sequence 0,1,2,3,0,1,2,3...

        Turning the encoder clockwise generates these
        values for switches B and A:
         B A
         0 0
         0 1
         1 1
         1 0
        We convert these to an ordinal sequence number by returning
          seq = (A ^ B) | B << 2
        """
        a_state = int(GPIO.input(self.__a_pin))
        b_state = int(GPIO.input(self.__b_pin))
        r_seq = (a_state ^ b_state) | b_state << 1
        return r_seq


    def get_delta(self):
        """
        Returns offset values of -2,-1,0,1,2
        """
        delta = 0
        r_seq = self.rotation_sequence()
        if r_seq != self.__r_seq:
            delta = (r_seq - self.__r_seq) % 4
            if delta==3:
                delta = -1
            elif delta==2:
                # same direction as previous, 2 steps
                delta = int(math.copysign(delta, self.__last_delta))

            self.__last_delta = delta
            self.__r_seq = r_seq

        return delta


    def update(self, _channel):
        """
        Callback that is called when either rotary encoder pin has changed
        values.
        """
        last_value = self.__raw_value / STEPS_PER_TICK
        self.__raw_value += self.get_delta()
        self.__raw_value = max(self.__raw_value, self.__min_raw_value)
        #if self.__max_raw_value is not None: self.__raw_value = min(self.__raw_value, self.__max_raw_value)
        self.__raw_value = min(self.__raw_value, self.__max_raw_value)
        new_value = self.__raw_value / STEPS_PER_TICK
        if new_value != last_value:
            self.__update_callback(new_value)


if __name__ == '__main__':
    def print_value(new_value):
        """
        Dummy value change method for testing.
        """
        print(f'Value changed to: {new_value}')

    GPIO.setmode(GPIO.BCM)

    a = RotaryEncoder(23, 24, callback=print_value)
    while True:
        time.sleep(1000)
