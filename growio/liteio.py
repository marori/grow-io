import argparse
from pyA20.gpio import gpio


class LiteIOException(Exception):
    pass


class UnavailablePin(LiteIOException):
    pass


class LiteIO(object):
    """This class provides basic GPIO read write for the OrangePi-Lite Board.

       LiteIO provides I/O based on the board pin numbers instead of the pyA20 gpio port names
    """
    _pin2bcm = {
        3:  12,
        5:  11,
        7:   6,   8: 13,
        10: 14,
        11:  1,  12: 110,
        13:  0,
        15:  3,  16: 68,
        18: 71,
        19: 64,
        21: 65,  22: 2,
        23: 66,  24: 67,
        26: 21,
        27: 19,  28: 18,
        29:  7,
        31:  8,  32: 200,
        33:  9,
        35: 10,  36: 201,
        37: 20,  38: 198,
        40: 199
    }

    def __init__(self, pin):
        """
        Initiate IO for given pin
        :param pin:n
        """
        if not pin in self._pin2bcm.keys():
            raise UnavailablePin("Pin %s is not available for I/O"%(pin))
        self.pin = pin
        self.bcm = self._pin2bcm[pin]
        gpio.init()
        gpio.pullup(self.bcm, gpio.PULLUP)

    def read(self):
        """Reads from GPIO pin
        :return: current pin value
        """
        gpio.setcfg(self.bcm, gpio.INPUT)
        return gpio.input(self.bcm)

    def write(self, value):
        """Writes to GPIO pin

        :param value: value to write
        """
        gpio.setcfg(self.bcm, gpio.OUTPUT)
        gpio.output(self.bcm, value)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Reads/Writes GPIO pin")
    parser.add_argument("pin", metavar="PIN", type=int, help="Board pin number")
    parser.add_argument("--write", metavar="VALUE", type=int, choices=[0, 1], help="write VALUE to PIN")
    args = parser.parse_args()

    lio = LiteIO(args.pin)

    if args.write is not None:
        lio.write(args.write)
    else:
        print(lio.read())
