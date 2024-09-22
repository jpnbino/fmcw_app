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
        """
        for i, value in enumerate(values):
            self.registers[ADDR_RAM_OFFSET + i] = value

    def get_default_config(self) -> list[int]:
        """
        Get the default configuration values.

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

    def reg_write(self, address: int, value: int, mask: int = 0xFFFF, shift: int = 0) -> int:
        """
        Write a value to a register based on the specified address, mask, and shift.

        Parameters:
        - address (int): The address of the register.
        - value (int): The value to write to the register.
        - mask (int): The mask to apply to the value.
        - shift (int): The shift to apply to the value.

        Returns:
        - int: The new value of the register.
        """
        if address >= ADDR_RAM_BEGIN:
            address = address - ADDR_RAM_BEGIN + ADDR_RAM_OFFSET

        byte0 = int(self.registers[address])
        byte1 = int(self.registers[address + 1])

        # Combine the two bytes into a 16-bit value
        tmp = (byte1 << 8) | byte0

        # Clear the bits in the register that correspond to the mask
        tmp &= ~(mask << shift)

        # Apply the mask and shift to the new value and combine with the cleared register value
        tmp |= (value & mask) << shift

        # Write the result back to the register
        self.registers[address] = tmp & 0xff
        self.registers[address + 1] = (tmp >> 8) & 0xff

        return tmp

    def reg_read(self, start_address: int, bit_shift: int = 0, bit_mask: int = 0xffff) -> int:
        """
        Extract a value from the ISL94203.registers list based on the specified parameters.

        Parameters:
        - start_address (int): The starting address of the ISL94203.
        - bit_shift (int): The bit shift for the value.
        - bit_mask (int): The bitmask for the value.

        Returns:
        - int: The extracted value.
        """
        if start_address >= ADDR_RAM_BEGIN:
            start_address = start_address - ADDR_RAM_BEGIN + ADDR_RAM_OFFSET

        # Assuming start_address points to the index in registers directly
        raw_value = (self.registers[start_address + 1] << 8) | self.registers[start_address]
        value = (raw_value >> bit_shift) & bit_mask
        return value

    def read_bit(self, address: int, bit_position: int) -> bool:
        """
        Extract a boolean value from ISL94203.registers based on the specified byte address and bit position.

        Parameters:
        - address (int): The byte address.
        - bit_position (int): The bit position within the byte.

        Returns:
        - bool: The boolean value.
        """
        # Extract the byte value from registers using read_reg_val
        byte_value = self.reg_read(address, 0, 0xff)

        # Calculate the boolean value based on the bit position
        return bool((byte_value >> bit_position) & 0x01)
