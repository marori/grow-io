import sys
import argparse
from smbus import SMBus
from time import sleep


class DACException(Exception):
    pass


class BadPort(DACException):
    pass


class BadAddress(DACException):
    pass


class DAC8591(object):
    """This class reads and writes from a DAC8591 DAC/ADC IC
    """
    def __init__(self, bus, addr):
        self.address = int(addr)
        self.bus = int(bus)

    def read(self, port):
        """Reads a value from the given ADC port
        :param port: The Analog port to read from
        :return: the byte read
        """
        if port < 0 or port > 3:
            raise BadPort("Port must be between 0 and 3")
        bus = SMBus(self.bus)
        bus.write_byte(self.address, port)
        bus.read_byte(self.address)
        sleep(2)
        return bus.read_byte(self.address)

    def write(self, value):
        """Writes a value to the DAC
        :param value: the byte value to write to the Analog Output
        """
        print("Not implemented yet... Write %s to %x" % (value, self.address))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Reads or writes to/from ADC/DAC")
    parser.add_argument("command", metavar="COMMAND", type=str, help="read/write")
    parser.add_argument("bus", metavar="BUS", type=int, help="the i2c bus (check with i2cdetect)")
    parser.add_argument("address", metavar="ADDRESS", type=str, help="the i2c address - dec or hex starting with 0x")
    parser.add_argument("port", metavar="PORT", type=int, help="input port", default=0)
    args = parser.parse_args()
    try:
        address = int(args.address)
    except ValueError:
        try:
            address = int(args.address, 16)
        except ValueError:
            print("The address must be an integer.")
            sys.exit(1)

    if args.command != 'read' and args.command != 'write':
        print("The command must be either 'read' or 'write'")
        
    dac = DAC8591(args.bus, address)
    print dac.read(args.port)
