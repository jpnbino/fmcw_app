from PySide6.QtCore import QObject, Signal, Slot, QByteArray, QTimer
from serialbsp.crc8 import calculate_crc, check_crc
from serialbsp.commands import *

MINIMUM_PACKET_SIZE = 3  # Minimum packet size (cmd, length, checksum)
MAXIMZE_PACKET_SIZE = 1024  # Maximum packet size


class SerialProtocolFmcw(QObject):
    """
    Handles encoding/decoding of serial communication for the FMCW system.
    """
    data_received = Signal(bytes)  # Signal for processed data received
    command_encoded = Signal(QByteArray)  # Signal for encoded command to send
    log_message = Signal(str)  # Signal for log messages
    error_occurred = Signal(str)  # Signal for errors

    def __init__(self, parent=None):
        super().__init__(parent)
        self.receive_buffer = bytearray()
        self.expected_response_cmd = None
        self.packet_timeout_timer = QTimer()
        self.packet_timeout_timer.setSingleShot(True)
        self.packet_timeout_timer.timeout.connect(self._handle_packet_timeout)
        self.packet_timeout = 100  # milliseconds

        # Timer for logging command and byte count every 5000ms
        self.logging_timer = QTimer()
        self.packet_timeout_timer.setSingleShot(True)
        self.logging_timer.timeout.connect(self._log_command_and_byte_count)
        self.logging_timeout = 5000  # milliseconds
        

    def encode_command(self, cmd: int, data: list[int]) -> None:
        """
        Encodes a command and its data into a byte array with checksum.

        Args:
        cmd: The command byte.
        data: A list of data bytes.
        """
        packet = [cmd] + data
        checksum = calculate_crc(packet + [0])
        packet.append(checksum)
        encoded_data = QByteArray(bytearray(packet))
        self.command_encoded.emit(encoded_data)
        self.expected_response_cmd = cmd  # Store the sent command       
        self.packet_timeout_timer.start(self.packet_timeout)  # Start the timeout
        
        self.logging_timer.start(self.logging_timeout)

    @Slot(bytes)
    def handle_raw_data(self, raw_data: bytes) -> None:
        """
        Handles raw data received from the serial port.
        This method is connected to the SerialManager's data_received signal.
        """
        self.receive_buffer.extend(raw_data)
        print("\nBuffer:", " ".join(f"0x{byte:02X}" for byte in self.receive_buffer))
        #self._try_extract_packets()

    def _try_extract_packets(self) -> None:
        while True:
            packet = self._extract_packet()
            if packet:
                self._process_packet(packet)
            else:
                break

    def _extract_packet(self) -> bytes | None:
        """
        Attempts to extract a complete packet from the receive buffer,
        using the expected response command as a guide.
        Clears the buffer if it exceeds the maximum allowed size.
        """
        if len(self.receive_buffer) > MAXIMZE_PACKET_SIZE:
            self.log_message.emit("Buffer exceeded maximum size, clearing buffer.")
            self.receive_buffer.clear()
            return None

        if self.expected_response_cmd is None:
            return None  # not expecting a response yet

        # Check if the first byte of the buffer is the expected command
        if not self.receive_buffer or self.receive_buffer[0] != self.expected_response_cmd:
            return None  # Command not found or not at the start of the buffer

        # Packet format [CMD DATA_ARRAY CHECKSUM]
        if len(self.receive_buffer) < MINIMUM_PACKET_SIZE:
            return None

        data_length = self.receive_buffer[1]
        expected_packet_length = 2 + data_length + 1

        if len(self.receive_buffer) < expected_packet_length:
            return None  # Wait for more data

        packet = bytes(self.receive_buffer[:expected_packet_length])
        self.receive_buffer.clear()  # Clear the entire buffer
        self.packet_timeout_timer.stop()  # Stop the timeout, we got the packet
        self.expected_response_cmd = None  # Reset
        return packet

    def _process_packet(self, packet: bytes) -> None:
        """
        Processes a complete packet (which is still in bytes).
        """
        try:
            # Attempt to decode as a string (if that makes sense for your data)
            decoded_string = packet.decode('utf-8')
            self.data_received.emit(decoded_string.encode('utf-8'))
            self.log_message.emit(f"Received text: {decoded_string}")
        except UnicodeDecodeError:
            # If decoding fails, handle as raw bytes
            self.data_received.emit(packet)
            self.log_message.emit(f"_process_packet: {' '.join(f'0x{byte:02X}' for byte in packet)}")

        # Example of further processing (replace with your logic):
        if len(packet) > 2:
            cmd = packet[0]
            data_length = packet[1]
            if len(packet) == 3 + data_length:
                data = packet[2: 2 + data_length]
                checksum = packet[2 + data_length]

                calculated_checksum = calculate_crc(list(packet[: 2 + data_length]))
                if checksum == calculated_checksum:
                    self.log_message.emit(f"Valid packet received. CMD: {cmd}, Data: {data.hex()}")
                    # Do something with cmd and data
                else:
                    self.error_occurred.emit(f"Checksum error in packet: {packet.hex()}")
            else:
                self.error_occurred.emit(f"Packet format error: {packet.hex()}")
        else:
            self.error_occurred.emit(f"Unknown packet type: {packet.hex()}")

    def _handle_packet_timeout(self) -> None:
        """
        Handles the case where we don't receive the expected response
        within the timeout period.
        """
        self.error_occurred.emit(f"Timeout waiting for response to CMD: {self.expected_response_cmd}")
        self.expected_response_cmd = None

    def _log_command_and_byte_count(self) -> None:
        """
        Logs the command and the number of bytes received in the buffer.
        This is called every 5000ms by the logging timer.
        """
        self.logging_timer.stop()
        if self.receive_buffer:
            cmd = self.receive_buffer[0] if len(self.receive_buffer) > 0 else None
            byte_count = len(self.receive_buffer)
            self.log_message.emit(f"Command: 0x{cmd:02X}, Bytes received: {byte_count}")
            self.log_message.emit(f"Data received:\n{' '.join(f'0x{byte:02X}' for byte in self.receive_buffer)}")
            self.receive_buffer.clear()
        else:
            self.log_message.emit("No data received in the last 5000ms.")