from bms.constants import Mask, MAX_ADDRESS
from bms.constants import ADDR_RAM_BEGIN, ADDR_RAM_OFFSET, DEFAULT_CONFIG


class ISL94203:
    """
    Class representing the ISL94203 battery management system IC.
    """

    def __init__(self):
        self.registers = [0] * len(DEFAULT_CONFIG)

    def set_registers(self, values: list[int]):
        """
        Set the register values.

        Parameters:
        - values (list[int]): List of values to set in the registers.
        """
        if len(values) != len(self.registers):
            raise ValueError(f"Invalid number of values: expected {len(self.registers)}, got {len(values)}")
        self.registers = values

    def get_registers(self) -> list[int]:
        """
        Get the current register values.

        Returns:
        - list[int]: List of current register values.
        """
        return self.registers

    def set_ram_values(self, values: list[int]):
        """
        Set the RAM values of the ISL94203.

        Parameters:
        - values (list[int]): List of values to set in the RAM.
                Raises:
        - IndexError: If the provided values list is too long.
        """
        if len(values) > len(self.registers) - ADDR_RAM_OFFSET:
            raise IndexError("Too many values for RAM")
        for i, value in enumerate(values):
            self.registers[ADDR_RAM_OFFSET + i] = value

    @staticmethod
    def get_default_config() -> list[int]:
        """
        Get the default configuration values as in the components datasheet.

        Returns:
        - list[int]: List of default configuration values.
        """
        return DEFAULT_CONFIG

    def get_config(self) -> list[int]:
        """
        Get the current configuration values.

        Returns:
        - list[int]: List of current configuration values.
        """
        return self.registers

    def reg_write(self, address: int, value: int, mask: Mask = Mask.MASK_16BIT, shift: int = 0) -> int:
        """
        Write a value to a register based on the specified address, mask, and shift.

        Parameters:
        - address (int): The address of the register.
        - value (int): The value to write to the register.
        - mask (Mask): The mask to apply to the value.
        - shift (int): The shift to apply to the value.

        Returns:
        - int: The new value of the register.
        """
        if not (0 <= address <= MAX_ADDRESS):
            raise ValueError(f"Invalid register address: {address}")

        if not (0 <= shift <= 15):
            raise ValueError(f"Invalid register shift: {shift}")

        # If the address is in the RAM region, adjust the address to the register index
        if address >= ADDR_RAM_BEGIN:
            address = address - ADDR_RAM_BEGIN + ADDR_RAM_OFFSET

        byte0 = int(self.registers[address])
        byte1 = int(self.registers[address + 1])

        # Combine the two bytes into a 16-bit value
        tmp = (byte1 << 8) | byte0

        # Clear the bits in the register that correspond to the mask
        tmp &= ~(mask.value << shift)

        # Apply the mask and shift to the new value and combine with the cleared register value
        tmp |= (value & mask.value) << shift

        # Write the result back to the register
        self.registers[address] = tmp & 0xff
        self.registers[address + 1] = (tmp >> 8) & 0xff

        return tmp

    def reg_read(self, address: int, shift: int = 0, mask: Mask = Mask.MASK_16BIT) -> int:
        """
        Read two consecutive registers and extracts a value based on the specified bit shift and bit mask.

        Treats the two bytes as a 16-bit value.

        Parameters:
        - address (int): The starting address of the ISL94203. (0x00-0xA9)
        - shift (int): Number of right shifts in value. (0-15)
        - mask (Mask): The bitmask for the value.

        Returns:
        - int: values after applying shift and mask.
        """
        if address < 0 or address > 0xA9:
            raise ValueError(f"Invalid address: {address}")

        if shift < 0 or shift > 15:
            raise ValueError(f"Invalid shift: {shift}")

        if address >= ADDR_RAM_BEGIN:
            address = address - ADDR_RAM_BEGIN + ADDR_RAM_OFFSET

        # Assuming start_address points to the index in registers directly
        raw_value = (self.registers[address + 1] << 8) | self.registers[address]
        value = (raw_value >> shift) & mask.value
        return value

    def read_bit(self, address: int, bit_position: int) -> bool:
        """
        Extract a bit value from the specified address.

        Parameters:
        - address (int): The byte address (0x00-0xA9).
        - bit_position (int): The bit position within the byte (0-7).

        Returns:
        - bool: The boolean value.
        """
        if address < 0 or address > 0xA9:
            raise ValueError(f"Invalid address: {address}")

        if bit_position < 0 or bit_position > 7:
            raise ValueError(f"Invalid bit position: {bit_position}")

        byte_value = self.reg_read(address, 0, Mask.MASK_8BIT)
        return bool((byte_value >> bit_position) & 0x01)
