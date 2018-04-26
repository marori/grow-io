import sys, argparse
from smbus import SMBus
from time import sleep

class DACException(Exception):
    pass
class BadPort(DACException):
    pass
class BadAddress(DACException):
    pass

class DAC8591():
    def __init__(self, bus, address):
        self.address = int(address)
        self.bus = int(bus)

    def read(self, port):
        """
        Reads a value from the given ADC port
        """
        if port < 0 or port > 3:
            raise BadPortException("Port must be between 0 and 3")
        bus = SMBus(self.bus)
        bus.write_byte(self.address, port)
        bus.read_byte(self.address)
        sleep(2)
        return bus.read_byte(self.address)

    def write(self, value):
        """
        Writes a value to the DAC
        """
        print("Not implemented yet...")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Reads or writes to/from ADC/DAC")
    parser.add_argument("command", metavar="COMMAND", type=str, help="read/write")
    parser.add_argument("bus", metavar="BUS", type=int, help="the i2c bus (check with i2cdetect)")
    parser.add_argument("address", metavar="ADDRESS", type=str, help="the i2c address (decimal, or hex starting with 0x)")
    parser.add_argument("port", metavar="PORT", type=int, help="input port", default=0)
    args = parser.parse_args()
    try:
        address = int(args.address)
    except:
        try:
            address = int(args.address, 16)
        except:
            print("The address must be an integer.")
            sys.exit(1)

    if args.command != 'read' and args.command != 'write':
        print("The command must be either 'read' or 'write'")
        
    dac = DAC8591(args.bus, address)
    print dac.read(args.port)
