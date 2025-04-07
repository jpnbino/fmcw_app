from PySide6.QtCore import QObject, Signal, Slot, QByteArray, QTimer
from serialbsp.crc8 import calculate_crc, check_crc
from serialbsp.commands import *
from time import time, sleep

MINIMUM_PACKET_SIZE = 3  # Minimum packet size (cmd, length, checksum)
MAXIMUM_PACKET_SIZE = 1024  # Maximum packet size


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
        self._expected_response_cmd = None
        self._expected_packet_length = None
        self._pending_response = None # Store the pending response from the last command

        # Timer for packet receive timeout
        self.packet_rx_timeout_timer = QTimer()
        self.packet_rx_timeout_timer.setSingleShot(True)
        self.packet_rx_timeout_timer.timeout.connect(self._handle_packet_timeout)
        self.packet_timeout = 4000  # milliseconds

        # Timer Used for debugging purposes to log the command and byte count
        self.dbg_logging_timer = QTimer()
        self.dbg_logging_timer.setSingleShot(True)
        self.dbg_logging_timer.timeout.connect(self._log_command_and_byte_count)
        self.logging_timeout = 5000 # milliseconds
        
    def read_packet(self, expected_size: int, timeout: float = 4.0) -> bytes:
        """
        Reads a specific number of bytes from the receive buffer.

        Args:
            expected_size (int): The number of bytes to read.
            timeout (float): The maximum time to wait for the bytes.

        Returns:
            bytes: The read bytes.

        Raises:
            TimeoutError: If the expected number of bytes is not received within the timeout.
        """
        start_time = time()
        while len(self.receive_buffer) < expected_size:
            print( len(self.receive_buffer), expected_size, time() - start_time, timeout)
            if time() - start_time > timeout:
                raise TimeoutError(f"Timeout waiting for {expected_size} bytes. Received {len(self.receive_buffer)} bytes.")
            sleep(1)
        packet = bytes(self.receive_buffer[:expected_size])
        del self.receive_buffer[:expected_size]
        return packet
    
    def encode_command(self, cmd: Command, data: list[int]) -> None:
        """
        Encodes a command and its data into a byte array with checksum.

        Args:
        cmd: The command byte.
        data: A list of data bytes.
        """
        self._expected_response_cmd = cmd.code
        self._expected_packet_length = cmd.response_size   

        packet = [cmd.code] + data
        checksum = calculate_crc(packet + [0])
        packet.append(checksum)
        encoded_data = QByteArray(bytearray(packet))
        self.command_encoded.emit(encoded_data)   
        self.packet_rx_timeout_timer.start(self.packet_timeout)
        
        #self.dbg_logging_timer.start(self.logging_timeout)

    @Slot(bytes)
    def handle_raw_data(self, raw_data: bytes) -> None:
        """
        Handles raw data received from the serial port.
        This method is connected to the SerialManager's data_received signal.
        """
        self.receive_buffer.extend(raw_data)
        #print("\nBuffer:\n", " ".join(f"0x{byte:02X}" for byte in self.receive_buffer))

        self._try_extract_packets()

    def _is_answer_to_command(self) -> bool:
        """
        Checks if the first byte of the receive buffer matches the expected response command.
        """
        if self._expected_response_cmd is not None and self.receive_buffer and self.receive_buffer[0] == self._expected_response_cmd:
            return True
        return False

    def _try_extract_packets(self) -> None: 
        while True:
            if self._is_answer_to_command():
                # Try to extract the expected response
                packet, consumed = self._extract_expected_packet()
                if packet:
                    self.log_message.emit(f"Rx: {' '.join(f'0x{byte:02X}' for byte in packet)}\n")
                    self._pending_response = packet # Store the response
                    self.data_received.emit(packet) # Still emit for potential further processing
                    if consumed > 0:
                        del self.receive_buffer[:consumed]
                    continue # Try to extract more packets
                else:
                    break # Need more data for the expected response
            else:
                # Try to extract an unsolicited message
                unsolicited_packet, consumed = self._extract_unsolicited_packet()
                if unsolicited_packet:
                    try:
                        decoded_message = unsolicited_packet.decode('utf-8', errors='ignore').strip()
                        if decoded_message:
                            self.log_message.emit(f"Unsolicited: {decoded_message}")
                            self.data_received.emit(unsolicited_packet) # Emit unsolicited data as well
                    except UnicodeDecodeError:
                        self.log_message.emit(f"Unsolicited (bytes): {' '.join(f'0x{byte:02X}' for byte in unsolicited_packet)}")
                        self.data_received.emit(unsolicited_packet)
                    if consumed > 0:
                        del self.receive_buffer[:consumed]
                    continue # Try to extract more packets
                else:
                    break # No more complete packets in the buffer
                break # If neither expected nor unsolicited could be extracted

    def _extract_expected_packet(self) -> tuple[bytes | None, int]:
        """
        Attempts to extract the expected response packet from the buffer.
        Returns the packet and the number of bytes consumed from the buffer.
        """
        if self._expected_response_cmd is None or self._expected_packet_length is None:
            return None, 0

        if len(self.receive_buffer) < MINIMUM_PACKET_SIZE:
            return None, 0

        # Assuming the expected packet has a fixed length
        if len(self.receive_buffer) >= self._expected_packet_length:
            packet = bytes(self.receive_buffer[:self._expected_packet_length])
            received_cmd = packet[0]
            if len(packet) >= MINIMUM_PACKET_SIZE:
                received_checksum = packet[-1]
                calculated_checksum = calculate_crc(list(packet[:-1]) + [0])
                if received_checksum == calculated_checksum and received_cmd == self._expected_response_cmd:
                    self.packet_rx_timeout_timer.stop()
                    return packet, self._expected_packet_length
                else:
                    self.log_message.emit(f"Checksum or Command mismatch for expected response. Received: 0x{received_checksum:02X}, Expected: 0x{calculated_checksum:02X}, Received CMD: 0x{received_cmd:02X}, Expected CMD: 0x{self._expected_response_cmd:02X}")
                    self._reset_receive_buffer()
                    return None, 1 # Consume at least one byte to avoid getting stuck
            else:
                return None, 1 # Consume at least one byte
        return None, 0 # Not enough data for the expected length

    def _reset_receive_buffer(self) -> None:
        """
        Resets the receive buffer and clears any expected response.
        """
        self.receive_buffer.clear()
        self._expected_response_cmd = None
        self._expected_packet_length = None
        self._pending_response = None
        self.packet_rx_timeout_timer.stop()  

    def _extract_unsolicited_packet(self) -> tuple[bytes | None, int]:
        """
        Attempts to extract an unsolicited string message from the buffer.
        Looks for valid UTF-8 encoded substrings delimited by a newline.
        Returns the packet and the number of bytes consumed.
        """
        if not self.receive_buffer or (self._expected_response_cmd is not None and self.receive_buffer[0] == self._expected_response_cmd):
            return None, 0

        try:
            decoded_buffer = self.receive_buffer.decode('utf-8', errors='ignore')
            if decoded_buffer:
                if '\n' in decoded_buffer:
                    end_index = decoded_buffer.find('\n')
                    unsolicited_message_bytes = self.receive_buffer[:end_index + 1]
                    return unsolicited_message_bytes, end_index + 1
                else:
                    if len(self.receive_buffer) > 2 * MAXIMUM_PACKET_SIZE:
                        self.log_message.emit("Potential runaway unsolicited message, clearing buffer.")
                        self.receive_buffer.clear()
                        return None, len(self.receive_buffer) # Consume the whole buffer
                    return None, 0
            else:
                return None, 1 # Consume at least one byte if decoding fails at the start
        except UnicodeDecodeError:
            return None, 1 # Consume at least one byte if decoding fails at the start

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

    def _handle_packet_timeout(self) -> None:
        """
        Handles the case where we don't receive the expected response
        within the timeout period.
        """
        if self._expected_response_cmd is not None:
            self.error_occurred.emit(f"Timeout waiting for response to CMD: 0x{self._expected_response_cmd:02X}")
            self._expected_response_cmd = None
            self._pending_response = None
            self.receive_buffer.clear()  # Clear the buffer to avoid confusion in the next command

    def _log_command_and_byte_count(self) -> None:
        """
        Debugging function to log the command and byte count every 5 seconds.
        This is useful for checking the command size without knowing it beforehand.
        """
        self.dbg_logging_timer.stop()
        if self.receive_buffer:
            cmd = self.receive_buffer[0] if len(self.receive_buffer) > 0 else None
            byte_count = len(self.receive_buffer)
            self.log_message.emit(f"[Debug]Command: 0x{cmd:02X}, Bytes received: {byte_count}")
            self.log_message.emit(f"[Debug] Data received:\n{' '.join(f'0x{byte:02X}' for byte in self.receive_buffer)}")
            self.receive_buffer.clear()
        else:
            self.log_message.emit("Data Rx Timeout.")
    