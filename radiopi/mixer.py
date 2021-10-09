"""
Defines methods for interacting with the mixer.
"""

import alsaaudio


MAX_VOLUME = 100


class Mixer:
    """
    Defines a basic mixer class that allows you to set a mixer volume based on
    a defined range.
    """
    def __init__(self, max_value=100):
        self.__mixer = alsaaudio.Mixer('PCM')
        self.__max_value = max_value

    def set_value(self, new_value):
        """
        Sets the mixer to the given value relative to the defined maximum.
        """
        new_volume = int(new_value * MAX_VOLUME / self.__max_value)

        print(f'Volume: {new_volume}%')
        self.__mixer.setvolume(new_volume)

    def get_value(self):
        """
        Retrieves the mixer's current value relative to the defined maximum.
        """
        volume = int(self.__mixer.getvolume()[0])

        return int(volume * self.__max_value / MAX_VOLUME)

    def turn_up(self):
        """
        Increases the volume by one step, doing nothing if it is already at the
        maximum.
        """
        old_volume = self.get_value()

        if old_volume < self.__max_value:
            self.set_value(old_volume + 1)

    def turn_down(self):
        """
        Decreases the volume by one step, doing nothing if it is already at the
        minimum.
        """
        old_volume = self.get_value()

        if old_volume > 0:
            self.set_value(old_volume - 1)



if __name__ == '__main__':
    mixer = Mixer(40)

    print(f'Mixer is (x/40): {mixer.get_value()}')

    print('Setting to 0/40')
    mixer.set_value(0)
    print(f'Mixer is (x/40): {mixer.get_value()}')

    print('Setting to 20/40)')
    mixer.set_value(20)
    print(f'Mixer is (x/40): {mixer.get_value()}')

    print('Setting to 40/40)')
    mixer.set_value(40)
    print(f'Mixer is (x/40): {mixer.get_value()}')
