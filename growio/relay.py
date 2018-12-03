import argparse
from liteio import LiteIO
import time

class RelayException(Exception):
    pass


class BadType(RelayException):
    pass


class Relay(object):
    """This class controls a Relay on the OrangePi-Lite Board with the following circuitry
                                  .
                                 /|\ Vcc
                                  |
                               | /
                       R       |V_
    LiteIO(Pin) O----/\/\/\----|    T
                               |\
                               | \
    Where:                        |--------O
      R = 1k                   |__|__
      T = PNP BC 307B             A  |
      D = 3.3v Zener         D   / \          Relay contacts
        3.3v Relay              /___\
                                  |--------O
                                 _|_
                                 /// Gnd
    """
    def __init__(self, pin, active_low=True):
        self.lio = LiteIO(pin)
        self.active_low = active_low
        self.state = False
        self.set_state(self.state)

    def set_state(self, on):
        """Sets relay on/off

        :param on: True if turning on relay
        """
        if type(on) != bool:
            raise BadType(RelayException)
        v = self.active_low
        if on:
            v = not self.active_low
        self.lio.write(v)
        self.state = on

    def on_during(self, seconds):
        """Sets state on for a given amount of seconds, turning off after they pass

        :param seconds:
        :return:
        """
        self.set_state(True)
        time.sleep(seconds)
        self.set_state(False)

    def get_state(self):
        """Gets current relay state
        :return: current state
        """
        return self.state

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sets relay on/off on a given pin")
    parser.add_argument("--active-high", action='store_true', help="Active high relay")
    parser.add_argument("pin", metavar="PIN", type=int, help="Board pin number")
    parser.add_argument("state", metavar="STATE", choices=['on', 'off'], help="Relay state [on|off]")

    args = parser.parse_args()

    relay = Relay(args.pin, not args.pullup_off)
    relay.set_state(args.state == 'on')
