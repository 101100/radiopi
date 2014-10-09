
import math
import time

import RPi.GPIO as GPIO

import alsaaudio


STEPS_PER_TICK = 4


class RotaryEncoder:
    #----------------------------------------------------------------------
    # Pass the wiring pin numbers here.  See:
    #  https://projects.drogon.net/raspberry-pi/wiringpi/pins/
    #----------------------------------------------------------------------
    def __init__(self, a_pin, b_pin, callback, startValue=0, minValue=0, maxValue=100):
        self.a_pin = a_pin
        self.b_pin = b_pin
        self.updateCallback = callback
        self.minRawValue = minValue * STEPS_PER_TICK
        self.maxRawValue = maxValue * STEPS_PER_TICK

        GPIO.setup(a_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
        GPIO.setup(b_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) 

        self.rawValue = startValue * STEPS_PER_TICK
        self.r_seq = self.rotation_sequence()

        GPIO.add_event_detect(a_pin, GPIO.BOTH, callback=self.update)
        GPIO.add_event_detect(b_pin, GPIO.BOTH, callback=self.update)


    # Returns the quadrature encoder state converted into
    # a numerical sequence 0,1,2,3,0,1,2,3...
    #    
    # Turning the encoder clockwise generates these
    # values for switches B and A:
    #  B A
    #  0 0
    #  0 1
    #  1 1
    #  1 0 
    # We convert these to an ordinal sequence number by returning
    #   seq = (A ^ B) | B << 2
    # 
    def rotation_sequence(self):
        a_state = int(GPIO.input(self.a_pin))
        b_state = int(GPIO.input(self.b_pin))
        r_seq = (a_state ^ b_state) | b_state << 1
        return r_seq


    # Returns offset values of -2,-1,0,1,2
    def get_delta(self):
        delta = 0
        r_seq = self.rotation_sequence()
        if r_seq != self.r_seq:
            delta = (r_seq - self.r_seq) % 4
            if delta==3:
                delta = -1
            elif delta==2:
                delta = int(math.copysign(delta, self.last_delta))  # same direction as previous, 2 steps
                
            self.last_delta = delta
            self.r_seq = r_seq

        return delta


    def update(self, channel):
        lastValue = self.rawValue / STEPS_PER_TICK
        self.rawValue += self.get_delta()
        self.rawValue = max(self.rawValue, self.minRawValue)
        #if self.maxRawValue is not None: self.rawValue = min(self.rawValue, self.maxRawValue)
        self.rawValue = min(self.rawValue, self.maxRawValue)
        newValue = self.rawValue / STEPS_PER_TICK
        if newValue != lastValue:
            self.updateCallback(newValue)


if __name__ == '__main__':
    def printValue(newValue):
        print 'Value changed to:', newValue

    GPIO.setmode(GPIO.BCM)

    a = RotaryEncoder(23, 24, callback=printValue)
    while True:
        time.sleep(1000)

