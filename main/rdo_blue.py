import time
import serial
import minimalmodbus

class RDO_Sensor():

    def __init__(self, dev="/dev/ttyS0"):
        instrument = minimalmodbus.Instrument(dev, 1)  # port name, slave address (in decimal)

        instrument.serial.port                     # this is the serial port name
        instrument.serial.baudrate = 19200         # Baud
        instrument.serial.bytesize = 8
        instrument.serial.parity   = serial.PARITY_EVEN
        instrument.serial.stopbits = 1
        instrument.serial.timeout  = 0.05          # seconds

        instrument.mode = minimalmodbus.MODE_RTU   # rtu or ascii mode
        instrument.clear_buffers_before_each_transaction = True
        instrument.debug = True

    def read_do(self):
        # Tal vez el registro que tengo que leer es 38 en lugar de 40038
        do_value = instrument.read_register(40038, 1)  # Read an integer from one 16-bit register in the slave
        print(do_value) # Verificar el rango de valores

    def read_temp(self):
        # Tal vez el registro que tengo que leer es 38 en lugar de 40038
        do_value = instrument.read_register(40046, 1)  # Read an integer from one 16-bit register in the slave
        print(do_value) # Verificar el rango de valores

    def read_do_sat(self):
        # Tal vez el registro que tengo que leer es 38 en lugar de 40038
        do_value = instrument.read_register(40054, 1)  # Read an integer from one 16-bit register in the slave
        print(do_value) # Verificar el rango de valores

    def read_ox_part_pre(self):
        # Tal vez el registro que tengo que leer es 38 en lugar de 40038
        do_value = instrument.read_register(40062, 1)  # Read an integer from one 16-bit register in the slave
        print(do_value) # Verificar el rango de valores

    def calibrate_live_salinity(self, value):
        # Write the Calibration Mode On command (0xE000) to the sensor command register.
        # Acá no se cual es el "sensor command register"

        # Update the live salinity registers if necessary
        instrument.write_register(40118, value, 1)

        # Prompt the user to place the instrument in a 100% saturation environment

        # Read the oxygen concentration and temperature parameters
        time.sleep(1)
        dif = 0
        do_value = self.read_do()
        while dif < 1:
            time.sleep(1)
            do_value = self.read_do()
            dif = do_value - dif

        dif = self.read_temp()
        while dif < 1:
            time.sleep(1)
            dif = dif - self.read_temp()

        # When these values have reached equilibrium
        # Record them in their respective 100% saturation calibration registers
        instrument.write_register(40118, value, 1)
