
import alsaaudio


MAX_VOLUME = 100


class Mixer:
    def __init__(self, maxValue=100):
        self.mixer = alsaaudio.Mixer('PCM')
        self.maxValue = maxValue

    def setValue(self, newValue):
        newVolume = newValue * MAX_VOLUME / self.maxValue

        print 'Volume: {}%'.format(newVolume)
        self.mixer.setvolume(newVolume)

    def getValue(self):
        volume = int(self.mixer.getvolume()[0])

        return int(volume * self.maxValue / MAX_VOLUME)



if __name__ == '__main__':
    mixer = Mixer(40)

    print 'Mixer is (x/40):', mixer.getValue()

    print 'Setting to 0/40'
    mixer.setValue(0)
    print 'Mixer is (x/40):', mixer.getValue()

    print 'Setting to 20/40'
    mixer.setValue(20)
    print 'Mixer is (x/40):', mixer.getValue()

    print 'Setting to 40/40'
    mixer.setValue(40)
    print 'Mixer is (x/40):', mixer.getValue()

