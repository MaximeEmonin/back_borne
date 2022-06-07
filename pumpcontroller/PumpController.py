import serial


class PumpController:
    def __init__(self) -> None:
        self.ser = serial.Serial("/dev/ttyUSB0", baudrate=9600)

    def command(self, tab):
        self.ser.write("-".join([str(i).rjust(2, "0") for i in tab]))

    def __del__(self):
        self.ser.close()
