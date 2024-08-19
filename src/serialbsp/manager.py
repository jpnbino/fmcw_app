from serial.tools import list_ports
from serialbsp.setup import SerialSetup


def get_available_ports():
    ports = list_ports.comports()
    return [(port.device, port.description) for port in ports]


def open_serial_port(port):
    try:
        serial_comm = SerialSetup()
        serial_comm.open_serial(port)
        return serial_comm
    except Exception as e:
        print(f"Error opening serial port: {e}")
        return None


def close_serial_port(serial_comm):
    if serial_comm:
        serial_comm.close_serial()
