import argparse
import time
import sys
from relay import *

class Light(object):
    """This class is to be used to controll a light
    It can be used to either switch on and off, or
    switching on for a given amount of time
    """

    def __init__(self, pin, active_low=True):
        self.relay = Relay(pin, active_low)

    def on(self):
        """Switches light on"""
        self.relay.set_state(True)

    def off(self):
        """Switches light off"""
        self.relay.set_state(False)

    def on_for(self, seconds):
        """Switches light on for a number of seconds

        :param seconds:
        :return:
        """
        self.relay.on_during(seconds)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Controls a light switch")
    parser.add_argument("--active-high", action='store_true', help="Active high relay")
    parser.add_argument("pin", metavar="PIN", type=int, help="Board pin number")
    parser.add_argument("on_off_seconds", metavar="ON_OFF_SECONDS", type=str, help="State to turn on light (on/off) or number of seconds to turn on")

    args = parser.parse_args()

    onoff = args.on_off_seconds

    light = Light(args.pin)

    try:
        seconds = int(onoff)
        light.on_for(seconds)
    except ValueError:
        if onoff != 'on' and onoff != "off":
            print("You should either set a state to turn on the light (on/off) or give a number of seconds to turn it on")
            sys.exit(1)
        if onoff == 'on':
            light.on()
        else:
            light.off()
