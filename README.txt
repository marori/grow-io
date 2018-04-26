This package provides the needed classes to use all the needed hardware on the Hidroponics grow board.

Note that because both Linux and Python are not suitable for real-time or time critical applications,
don't use this if you need that!! Couple your *Pi to an arduino if that's really needed.

Dependencies:
This package uses python i2c implementation from smbus, so make sure the kernel module pcf8591 is not loaded (add it to blacklist).

The temperature sensor uses the kernel modules w1_sunxi, w1-gpio and w1_therm, make sure to load them.



