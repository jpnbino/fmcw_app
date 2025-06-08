from PySide6.QtCore import QObject, Signal, Slot, QThread
import serial
from serial.tools import list_ports
from serial import SerialException


class SerialManager(QObject):
    """
    Manages the serial port connection and communication.
    """

    data_received = Signal(bytes)  # Signal for raw data received
    connection_status_changed = Signal(bool)
    error_occurred = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.serial_port = serial.Serial()
        self.read_thread = QThread()
        self.reader = SerialPortReader()
        self.reader.moveToThread(self.read_thread)
        self.reader.data_received.connect(self.data_received)
        self.reader.error_occurred.connect(self.error_occurred)
        self.reader.connection_status_changed.connect(self.connection_status_changed)

        # Start the reader when the thread starts
        self.read_thread.started.connect(self.reader.run)
        self.current_port = None
        print("SerialManager is running")

    def get_available_ports(self) -> list[tuple[str, str, str, str]]:
        """
        Returns a list of available serial ports with their descriptions, VID, and PID.

        Returns:
            list[tuple[str, str, str, str]]: A list of tuples containing port name, description, VID, and PID.
        """
        ports = list_ports.comports()
        available_ports = []
        for port in ports:
            vid = f"{port.vid:04X}" if port.vid else None
            pid = f"{port.pid:04X}" if port.pid else None
            available_ports.append((port.device, port.description, vid, pid))
        return available_ports

    def open_serial_port(self, port: str, baudrate: int = 9600, timeout: float = 2) -> None:
        """Opens the specified serial port."""
        self.serial_port.port = port
        self.serial_port.baudrate = baudrate
        self.serial_port.timeout = timeout
        self.current_port = port
        try:
            self.serial_port.open()

            # If the thread is not running, create a new thread and a new reader
            if not self.read_thread.isRunning():
                self.read_thread = QThread()
                self.reader = SerialPortReader()  # <-- Create a new instance!
                self.reader.set_serial_port(self.serial_port)
                self.reader.moveToThread(self.read_thread)
                self.read_thread.started.connect(self.reader.run)
                self.reader.data_received.connect(self.data_received)
                self.reader.error_occurred.connect(self.error_occurred)
                self.reader.connection_status_changed.connect(self.connection_status_changed)
                self.read_thread.start()
            else:
                self.reader.set_serial_port(self.serial_port)
            self.connection_status_changed.emit(True)
        except SerialException as e:
            self.error_occurred.emit(f"Error opening serial port: {e}")
            self.connection_status_changed.emit(False)

    def close_serial_port(self) -> None:
        """Closes the currently open serial port."""
        try:
            if self.serial_port.is_open:
                self.stop_reading()
                try:
                    self.serial_port.close()
                    self.current_port = None
                except Exception as e:
                    self.error_occurred.emit(f"Error closing serial port: {e}")
                self.serial_port.port = None
        finally:
            # Always emit status change, even if already closed or error
            self.connection_status_changed.emit(False)

    def is_open(self) -> bool:
        """Returns True if the serial port is currently open."""
        return self.serial_port.is_open

    def send_data(self, data: bytes) -> None:
        """Sends raw bytes over the serial port."""
        try:
            if self.serial_port.is_open:
                self.serial_port.write(data)
            else:
                self.error_occurred.emit("Serial port is not open")
        except SerialException as e:
            self.error_occurred.emit(f"Error sending data: {e}")

    def stop_reading(self) -> None:
        """Stops the serial reading thread."""
        if self.reader:
            self.reader.stop()
        if self.read_thread.isRunning():
            self.read_thread.quit()
            self.read_thread.wait()
        if self.reader:
            self.reader.set_serial_port(None)
            self.reader = None

    def reset_input_buffer(self) -> None:
        """Clears the input buffer of the serial port."""
        if self.serial_port.is_open:
            self.serial_port.reset_input_buffer()

    def reset_output_buffer(self) -> None:
        """Clears the output buffer of the serial port."""
        if self.serial_port.is_open:
            self.serial_port.reset_output_buffer()


class SerialPortReader(QObject):
    """
    Reads data from the serial port in a separate thread.
    """

    data_received = Signal(bytes)
    error_occurred = Signal(str)
    connection_status_changed = Signal(bool) 

    def __init__(self):
        super().__init__()
        self.serial_port = None
        self._stop_flag = False

    def stop(self):
        """Sets the stop flag to exit the reading loop."""
        self._stop_flag = True

    @Slot()
    def run(self) -> None:
        """
        Continuously reads data from the serial port.
        This method should be called when the QThread starts.
        """
        self._stop_flag = False 
        print("SerialPortReader: run() started")
        while self.serial_port and self.serial_port.is_open and not self._stop_flag:
            try:
                data = self.serial_port.read_all()
                if data:
                    self.data_received.emit(data)

            except SerialException as e:
                self.error_occurred.emit(f"Serial exception: {e}")
                if self.serial_port and self.serial_port.is_open:
                    self.serial_port.close()
                self.connection_status_changed.emit(False) 
                break  # Exit the loop on error
        print("SerialPortReader: run() stopped")

    def set_serial_port(self, serial_port: serial.Serial) -> None:
        """Sets the serial port for the reader."""
        self.serial_port = serial_port
        