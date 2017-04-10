This project holds code to make a Raspberry Pi internet radio.

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

There are only a few radio stations in the list, but more can be added by making
a `streams.json` file with a format like `streams-example.json`.

