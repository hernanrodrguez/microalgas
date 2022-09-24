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
