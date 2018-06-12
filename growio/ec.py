import argparse
import sys
from dac import DAC8591
from temp import Therm
from liteio import LiteIO


class EcMeterException(Exception):
    pass


class InvalidParameter(EcMeterException):
    pass


class EcMeter(object):
    """This class reads the Electric Conductivity

   To measure the EC, we use a US power plug as probe, and a DS18B20 temperature sensor
   Two GPIO pins (S1, S2) are used to control power sources to simulate alternate current
   A DAC8591 is used to measure the voltage on the power plug
   A Thermometer is needed to adjust the measurement for temperature

             Ri               Ra
   S1 _____/\/\/\___________/\/\/\_______
                                         |            _______
                                         |           |       |
                                         |____ Vo ___|  ADC  |____
                           o Probe o     |           |_______|
             Ri            |       |     |
   S2 _____/\/\/\__________|   Rw  |_____|

   Where S1 and S2 are GPIO Outputs, to be used as 3.3V alternating input source (S2 = !S1)
   Ri are the internal OrangePi resistor, which we can't change.
   Ra is found empirically to be best at ~500ohm
   The Plug goes into the water, knowing Vo we can calculate Rw (Resistance of Water)
    """
    temperature_compensation = 0.019 # typical temp compensation for hydroponic solutions
    calibration = 0.2

    def __init__(self, s1, s2, adc, adc_port, temp, calibration=None):
        """Initiates an EC meter

        :param s1: LiteIO(pin1) - input source 1
        :param s2: LiteIO(pin2) - input source 2
        :param adc: DAC8591(bus, addr) - the ADC instance
        :param adc_port: int   - the analog port from the ADC
        :param temp: Therm(device_id) - the water temperature meter
        """
        if not isinstance(s1, LiteIO):
            raise InvalidParameter("Output S1 must be a valid LiteIO object")
        if not isinstance(s2, LiteIO):
            raise InvalidParameter("Output S2 must be a valid LiteIO object")
        if not isinstance(adc, DAC8591):
            raise InvalidParameter("Analog to Digital Converter adc must be a valid DAC8591 object")
        if not isinstance(adc_port, int):
            raise InvalidParameter("Analog port must be integer")
        if not isinstance(temp, Therm):
            raise InvalidParameter("Temperature sensor must be a valid Therm object")
        if isinstance(calibration, float):
            self.calibration = calibration

        self.s1 = s1
        self.s2 = s2
        self.adc = adc
        self.adc_port = adc_port
        self.temp = temp

    def read(self):
        """Reads the Electrical Conductivity

        :return: EC measurement results in siemens
        """
        tc = EcMeter.temperature_compensation
        temp = self.temp.read()
        self.s1.write(0)
        self.s2.write(1)
        v1 = self.adc.read(self.adc_port)
        self.s1.write(1)
        self.s2.write(0)
        v2 = self.adc.read(self.adc_port)
        self.s1.write(0)

        #print([v1, v2])
        v = sum([255 - v1, v2]) / 2
        print v
        print "ec25 = v * self.calibration / (1 + tc*(temp-25.0)) "
        ec25 = v * self.calibration / (1 + tc*(temp-25.0))
        print "%s = %s * %s / (1 + %s * (%s - 25.0))" % (
            ec25, v, self.calibration, tc, temp
        )
        return ec25

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Read the EC of water.")
    parser.add_argument("S1", metavar="S1", type=int, help="Input source board pin 1")
    parser.add_argument("S2", metavar="S2", type=int, help="Input source board pin 2")
    parser.add_argument("bus", metavar="I2CBUS", type=int, help="I2C bus - use i2cdetect")
    parser.add_argument("addr", metavar="I2CADDRESS", type=str, help="I2C ADC address - use i2cdetect")
    parser.add_argument("port", metavar="PORT", type=int, help="Analog port")
    parser.add_argument("device_id", metavar="DEVICE_ID", type=str, help="Temperature sensor device ID")

    args = parser.parse_args()

    # parse Source Pins

    # parse Bus
    
    # parse address
    try:
        address = int(args.addr)
    except ValueError:
        try:
            address = int(args.addr, 16)
        except ValueError:
            print("The address must be an integer.")
            sys.exit(1)

    # parse adc port (between 1 and 4)

    # parse temperature device ID
    
