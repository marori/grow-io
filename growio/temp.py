import argparse
import os
import sys


class ThermException(Exception):
    pass


class DeviceNotFound(ThermException):
    pass


class ReadingFailed(ThermException):
    pass


class Therm(object):
    w1_master_path = "/sys/devices/w1_bus_master1"
    
    @staticmethod
    def list_devices():
        master_slaves = open("%s/w1_master_slaves" % Therm.w1_master_path, 'r')
        slaves = map(str.strip, master_slaves.readlines())
        return slaves
    
    def __init__(self, device_id):
        if not os.path.isdir("%s/%s" % (self.w1_master_path, device_id)):
            raise DeviceNotFound("Device %s not found" % device_id)
        self.device_id = device_id

    def read(self):
        """
        Reads the temperature value
        """
        # we do up to 10 tries to get 5 readings to make an average
        tries = 10
        success_reads = 0
        readings = []
        success = False
        while tries > 0:
            reading = open("%s/%s/w1_slave" % (self.w1_master_path, self.device_id), 'r')
            results = reading.readlines()
            crc = results[0].strip()[-3:]
            if crc == "YES":
                success_reads += 1
                
                temp = int(results[1][results[1].rfind('=')+1:].strip())
                readings.append(temp)
                if success_reads == 5:
                    success = True
                    break
            tries -= 1
        if success:
            average = sum(readings)/5000.0
            return average
        raise ReadingFailed("Maximum amount of tries exceeded...")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Reads the temperature value from a given thermometer")
    parser.add_argument('-l', action='store_true', help="list devices")
    parser.add_argument('-a', action='store_true', help="read from all devices")
    parser.add_argument("device_id", nargs='?', metavar="DEVICE_ID", type=str, default=None,
                        help="The device ID can be found at /sys/devices/w1_bus_master")

    def p(s):
        print(s)

    args = parser.parse_args()
    if args.l:
        map(p, Therm.list_devices())
        sys.exit(0)

    if args.a:
        devices = Therm.list_devices()
        therms = [Therm(device) for device in devices]
        temps = ["%s -- %s" % (therm.device_id, therm.read()) for therm in therms]
        map(p, temps)
        sys.exit(0)

    if args.device_id is None:
        print("You must provide a device ID")
        parser.print_usage()
        sys.exit(2)

    try:
        therm = Therm(args.device_id)
    except DeviceNotFound as e:
        print(e.message)
        sys.exit(1)
        
    print(therm.read())
