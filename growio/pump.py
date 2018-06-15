import argparse
from relay import *

class Pump(Relay):
    """This class is to be used with a water pump connected to a Relay
    it's used to turn on a pump for a given amount of time
    """
    def __init__(self, pin, active_low=True):
        self.relay = Relay(pin, active_low)

    def pump_for(self, seconds):
        """Sets the pump on for a given number of seconds

        :param seconds:
        :return:
        """
        self.on_during(seconds)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sets a pump on for a given number of seconds")
    parser.add_argument("--active-high", action='store_true', help="Active high relay connected to the pump")
    parser.add_argument("pin", metavar="PIN", type=int, help="Board pin number")
    parser.add_argument("seconds", metavar="SECONDS", type=int, help="Seconds to keep the pump on")

    args = parser.parse_args()

    pump = Pump(args.pin)
    pump.pump_for(args.seconds)
    