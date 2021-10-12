This project holds code to make a Raspberry Pi internet radio.

# Overview

I put a Raspberry Pi, Wifi dongle, [simple
amplifier](http://www.adafruit.com/products/987), and a [rotary
encoder](http://www.adafruit.com/product/377) into an old bookshelf speaker.

The rotary encoder pins (the three on one side) are connected to pins 23 and 24
and to ground.  The ground should be connected to the middle pin, the other two
can be in either order.  The button pins (the two on one side) are connected to
pin 18 and to ground (the order doesn't matter).  These pins can be adjusted in
`__main__.py`

The encoder adjusts volume and turns it on or off.  Each time you press the
button it alternates between off and a random radio station.

It also says the name of the station and the city as it turns on.

There are only a few radio stations in the list by default, but more can be added
by making or using some of the `streams-*.json` files in the repo.

# Installation

1. Configure your Raspberry Pi with the network credentials it will need to
   connect to your wireless network.
1. Configure the audio to always use the 3.5 mm audio jack.
1. Install the required debian packages:
   `sudo apt install git tmux mpd mpg123 python3-alsaaudio python3-mpd python3-pip`
   - `git` to get the project code
   - `tmux` to run the project in
   - `mpd` to play the radio streams
   - `mpg123` to play the announcement MP3s from Amazon Polly
   - `python3-alsaaudio` to control the volume
   - `python3-mpd` to control `mpd`
   - `python3-pip` to allow us to install python packages using `pip3`
1. Install the required PIP packages:
   `sudo pip3 install boto3`
1. `git clone https://github.com/101100/radiopi.git`
1. Edit `~/radiopi/runRadioPi.sh` with the required Amazon credentials to use
  for Amazon Polly.
1. Edit and copy as many of the `streams-*.json` files as you would like into
   `~/radiopi/radiopi` to add stations you want. Each press that turns on the
   radio will alternate between the different files allowing you to alternate
   between Art Bell and old radio shows, for example.
1. Manually run `~/radiopi/runRadioPi.sh` and ensure everything works.
1. Configure `~/radiopi/runRadioPi.sh` or `~/radiopi/tmuxRadioPi.sh` to be run
   on startup. For example, you could add these lines to `/etc/rc.local`:
   ```sh
   echo -n "Running radiopi..."
   sudo -u pi bash /home/pi/radiopi/tmuxRadioPi.sh
   echo " done."
   ```
1. Restart your Pi and ensure you hear "Radio Pi Started"

## Fixing the mixer with Pimoroni Pirate Audio

Some cards have no mixer support in ALSA. In this case, you can use software
volume control by creating an ALSA config file in `/etc/asound.conf`. Here is
what it might look like:

```
pcm.!default {
  type plug
  slave.pcm "tester"
}

ctl.!default  {
  type hw
  card sndrpihifiberry
}

pcm.tester {
  type softvol
  slave.pcm "plughw:CARD=sndrpihifiberry"
  control.name "PCM"
  control.card 0
}
```