"""Formula AllCode Robot Buggy functions"""


import time
import serial as _serial
import sys as _sys
from sys import platform as _platform


if _platform == "win32":
    if (_sys.version_info.major == 2):
        import _winreg as _winreg
    else:
        import winreg as _winreg


class Create:
    __ser = _serial.Serial()
    __verbose = 0
    
    def __init__(self):
        self.__ser.close()
        return;
    
    def ComOpen(self, port):
        """Open a communication link to the robot

        Args:
            port: The COM port to open
        """
        
        if _platform == "linux" or _platform == "linux2":
            # linux
            s = '/dev/rfcomm{0}'.format(port)
        elif _platform == "darwin":
            # MAC OS X
            print("Error - MAC OS TODO")
        elif _platform == "win32":
            # Windows
            s = '\\\\.\\COM{0}'.format(port)
        else:
            print("Error - unsupported platform")

        self.__ser = _serial.Serial(port=s,\
                            baudrate=115200,\
                            parity=_serial.PARITY_NONE,\
                            stopbits=_serial.STOPBITS_ONE,\
                            bytesize=_serial.EIGHTBITS,\
                            timeout=1)
        #TODO: add checking to ensure port is open
        return;

    def ComClose(self):
        """Close the communication link to the robot
        """
        self.__ser.close()
        return;

##    def _comlist(self):
##        #TODO: this is Windows-only at the moment
##        if _platform == "win32":
##            key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, 'HARDWARE\\DEVICEMAP\\SERIALCOMM')
##            i = 0
##            while True:
##                try:
##                    name = _winreg.EnumValue(key, i)[1][3:]
##                except OSError:
##                    #no more COM ports
##                    break
##                yield name #, '\\\\.\\{0}'.format(name)
##                i += 1
##
##            _winreg.CloseKey(key)
        
##    def ComQuery(self, port):
##        #TODO
##        comlist = self._comlist()
##        print (comlist)
##        return;
##
##    def ComFindFirst(self):
##        #TODO
##        return;

##    def Test(self):
##        #TODO: this is Windows-only at the moment
##        key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, 'HARDWARE\\DEVICEMAP\\SERIALCOMM')
##        i = 0
##        while True:
##            try:
##                name = _winreg.EnumValue(key, i)[1][3:]
##            except OSError:
##                #no more COM ports
##                break
##            yield name #, '\\\\.\\{0}'.format(name)
##            i += 1
##
##        _winreg.CloseKey(key)
    
    
    def _readval(self, cmd, loop_max):
        r = -1
        loop = 0
        while (loop < loop_max):
            try:
                r = int(self.__ser.readline().rstrip())
                if (self.__verbose != 0):
                    msg = '{0}: {1}'.format(cmd, r)
                    print(msg)
                loop = loop_max + 1   #break out of loop
            except ValueError:
                if (self.__verbose != 0):
                    msg = '{0}: No return({1})'.format(cmd,loop)
                    print(msg)
            loop = loop + 1
        return(r);

    def _flush(self):
        count = self.__ser.in_waiting
        while (count > 0):
            self.__ser.readline().rstrip()
            count = self.__ser.in_waiting
        return;

    def _set_verbose(self, value):
        self.__verbose = value
        return;





    def ADCSample8(self, channel):
        """Reads an analogue value from a pin as an 8-bit value

        Args:
            channel: The pin to read to (0 to 2)

        Returns:
            The voltage of the pin (0 to 255)
        """
        self._flush()
        values = bytearray([0x9B, channel, 0])
        self.__ser.write(values)
        values = self.__ser.read(3)
        return(values[2]);

    def ADCSample10(self, channel):
        """Reads an analogue value from a pin as a 10-bit value

        Args:
            channel: The pin to read to (0 to 2)

        Returns:
            The voltage of the pin (0 to 1023)
        """
        self._flush()
        values = bytearray([0x9C, channel, 0, 0])
        self.__ser.write(values)
        values = self.__ser.read(4)
        r = (values[2] * 256) + values[3]
        return(r);

    def DACDisable(self):
        """Disables the DAC output
        
        """
        self._flush()
        values = bytearray([0x9E])
        self.__ser.write(values)
        values = self.__ser.read(1)
        return;

    def DACEnable(self):
        """Enables the DAC output
        
        """
        self._flush()
        values = bytearray([0x9D])
        self.__ser.write(values)
        values = self.__ser.read(1)
        return;

    def DACOutput(self, value):
        """Writes a 5-bit value to the DAC output
        
        Args:
            value: The value to write to (0 to 31)
        
        """
        self._flush()
        values = bytearray([0x9F, value])
        self.__ser.write(values)
        values = self.__ser.read(2)
        return;

    def I2CInitialise(self):
        """Enables the I2C interface
        
        """
        self._flush()
        values = bytearray([0x86])
        self.__ser.write(values)
        values = self.__ser.read(1)
        return;

    def I2CReceive(self, last):
        """Reads an byte from the I2C interface
        
        Args:
            last: The last byte to read? (0 to 1)

        Returns:
            The received value (0 to 255)
        """
        self._flush()
        values = bytearray([0x8B, last, 0])
        self.__ser.write(values)
        values = self.__ser.read(3)
        return(values[2]);

    def I2CRestart(self):
        """Restarts the I2C interface
        
        """
        self._flush()
        values = bytearray([0x88])
        self.__ser.write(values)
        values = self.__ser.read(1)
        return;

    def I2CSend(self, data):
        """Sends a byte to the I2C interface

        Args:
            data: The last byte to send (0 to 255)

        Returns:
            The ack value (0 to 1)
        """
        self._flush()
        values = bytearray([0x8A, data, 0])
        self.__ser.write(values)
        values = self.__ser.read(3)
        return(values[2]);

    def I2CStart(self):
        """Starts the I2C interface
        
        """
        self._flush()
        values = bytearray([0x87])
        self.__ser.write(values)
        values = self.__ser.read(1)
        return;

    def I2CStop(self):
        """Stops the I2C interface
        
        """
        self._flush()
        values = bytearray([0x89])
        self.__ser.write(values)
        values = self.__ser.read(1)
        return;

    def IOGetInputPin(self, pin):
        """Reads a value from a pin

        Args:
            pin: The pin to write to (0 to 17)

        Returns:
            The state of the pin (0 to 1)
        """
        self._flush()
        values = bytearray([0x81, pin, 0])
        self.__ser.write(values)
        values = self.__ser.read(3)
        return(values[2]);

    def IOSetOutputPin(self, pin, state):
        """Write a value to a pin

        Args:
            pin: The pin to write to (0 to 17)
            state: The value to output (0 to 1)
        """
        self._flush()
        values = bytearray([0x80, pin, state])
        self.__ser.write(values)
        self.__ser.read(3)
        return;   

    def PWMDisable(self, channel):
        """Disables one of the PWM output channels

        Args:
            channel: The PWM channel to disable (0 to 1)

        """
        self._flush()
        values = bytearray([0x93, channel])
        self.__ser.write(values)
        values = self.__ser.read(2)
        return;

    def PWMEnable(self, channel):
        """Enables one of the PWM output channels

        Args:
            channel: The PWM channel to enable (0 to 1)

        """
        self._flush()
        values = bytearray([0x92, channel])
        self.__ser.write(values)
        values = self.__ser.read(2)
        return;

    def PWMSetDuty8(self, channel, value):
        """Sets the duty one of the PWM output channels as an 8-bit value

        Args:
            channel: The PWM channel to enable (0 to 1)
            value: The duty of the PWM channel (0 to 255)

        """
        self._flush()
        values = bytearray([0x95, channel, value])
        self.__ser.write(values)
        values = self.__ser.read(3)
        return;

    def PWMSetDuty10(self, channel, value):
        """Sets the duty one of the PWM output channels as a 10-bit value

        Args:
            channel: The PWM channel to enable (0 to 1)
            value: The duty of the PWM channel (0 to 1023)

        """
        lsb = value & 255 
        msb = value / 256
        self._flush()
        values = bytearray([0x96, channel, lsb, msb])
        self.__ser.write(values)
        values = self.__ser.read(4)
        return;

    def PWMSetPrescaler(self, scaler):
        """Sets the prescaler of the PWM output channels

        Args:
            scaler: The scaler of the PWM channels (0 to 3) 0=1:1 1=1:4 2=1:16 3=1:64

        """
        self._flush()
        values = bytearray([0x94, scaler])
        self.__ser.write(values)
        values = self.__ser.read(2)
        return;

    def SPIInitialise(self):
        """Enables the SPI interface
        
        """
        self._flush()
        values = bytearray([0x82])
        self.__ser.write(values)
        values = self.__ser.read(1)
        return;

    def SPIPrescaler(self, scaler):
        """Sets the prescaler of the SPI interface

        Args:
            scaler: The scaler of the SPI interface (0 to 2) 0=1:1 1=1:4 2=1:16

        """
        self._flush()
        values = bytearray([0x85, scaler])
        self.__ser.write(values)
        values = self.__ser.read(2)
        return;

    def SPITransfer(self, data):
        """Reads and writes a byte on the SPI interface

        Args:
            data: The data byte to send (0 to 255)
            
        Returns:
            The received value (0 to 255)
        """
        self._flush()
        values = bytearray([0x83, data, 0])
        self.__ser.write(values)
        values = self.__ser.read(3)
        return(values[2]);

    def ServoDisable(self, channel):
        """Disables one of the Servo output channels

        Args:
            channel: The Servo channel to disable (0 to 5)

        """
        self._flush()
        values = bytearray([0x98, channel])
        self.__ser.write(values)
        values = self.__ser.read(2)
        return;

    def ServoEnable(self, channel):
        """Enables one of the Servo output channels

        Args:
            channel: The Servo channel to enable (0 to 5)

        """
        self._flush()
        values = bytearray([0x97, channel])
        self.__ser.write(values)
        values = self.__ser.read(2)
        return;

    def ServoSetPosition8(self, channel, position):
        """Sets the position one of the servo output channels as an 8-bit value

        Args:
            channel: The Servo channel to enable (0 to 1)
            position: The position of the Servo channel (0 to 255)

        """
        self._flush()
        values = bytearray([0x99, channel, position])
        self.__ser.write(values)
        values = self.__ser.read(3)
        return;

    def ServoSetPosition16(self, channel, position):
        """Sets the position one of the servo output channels as an 16-bit value

        Args:
            channel: The Servo channel to enable (0 to 1)
            position: The position of the Servo channel (0 to 65535)

        """
        lsb = position & 255 
        msb = position / 256
        self._flush()
        values = bytearray([0x9A, channel, lsb, msb])
        self.__ser.write(values)
        values = self.__ser.read(4)
        return;

    def UARTBaud(self, rate):
        """Sets the baud rate of the UART interface

        Args:
            rate: The baud rate of the UART interface (0 to 7) 0=1200, 1=2400, 2=4800, 3=9600, 4=19200, 5=38400, 6=57600, 7=115200

        """
        self._flush()
        values = bytearray([0x91, rate])
        self.__ser.write(values)
        values = self.__ser.read(2)
        return;

    def UARTInitialise(self):
        """Enables the UART interface
        
        """
        self._flush()
        values = bytearray([0x8D])
        self.__ser.write(values)
        values = self.__ser.read(1)
        return;

    def UARTReceive(self):
        """Reads a byte from the UART receive buffer
            
        Returns:
            The received value (0 to 255)
        """
        self._flush()
        values = bytearray([0x90, 0])
        self.__ser.write(values)
        values = self.__ser.read(2)
        return(values[1]);

    def UARTReceiveCount(self):
        """Reads the number of bytes stored in the UART receive buffer
            
        Returns:
            The received value (0 to 255)
        """
        self._flush()
        values = bytearray([0x8F, 0])
        self.__ser.write(values)
        values = self.__ser.read(2)
        return(values[1]);

    def UARTTransmit(self, data):
        """writes a byte to the UART interface

        Args:
            data: The data byte to send (0 to 255)
            
        """
        self._flush()
        values = bytearray([0x8E, data])
        self.__ser.write(values)
        values = self.__ser.read(2)
        return;


