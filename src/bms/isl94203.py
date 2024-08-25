from bms.constants import ADDR_RAM_BEGIN, ADDR_RAM_OFFSET, DEFAULT_CONFIG
import logging

class ISL94203:
    registers = [0] * len(DEFAULT_CONFIG)

    def __init__(self):
        pass

    # Assuming the values get 16bits, therefore, operations are over two consecutives addresses 
    # example:
    def reg_set_all_values(self, values):
        ISL94203.registers = values

    def get_default_config(self):
        return DEFAULT_CONFIG

    def get_config(self):
        return self.registers
    
    def reg_write(self, address, value, mask=0xFFFF, shift=0):
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

    def reg_read(self, start_address, bit_shift=0, bit_mask=0xffff):
        """
        Extracts a value from the ISL94203.registers list based on the specified parameters.

        This function considers the offset between the RAM addresses and the actual index in the 'registers' list.

        Parameters:
        - start_address (int): The starting address of the ISL94203. If the address is in RAM,
        it is converted to the actual index in 'registers'.
        - bit_shift (int): The bit shift for the value.
        - bit_mask (int): The bitmask for the value.

        Returns:
        - int: The extracted value.
        """
        if start_address >= ADDR_RAM_BEGIN:
            start_address = start_address - ADDR_RAM_BEGIN + ADDR_RAM_OFFSET

        # Assuming start_address points to the index in registers directly
        raw_value = (ISL94203.registers[start_address + 1] << 8) | ISL94203.registers[start_address]
        value = (raw_value >> bit_shift) & bit_mask
        return value

    def read_bit(self, address, bit_position):
        """
        Extracts a boolean value from ISL94203.registers based on the specified byte address and bit position.

        Parameters:
        - byte_address (int): The byte address.
        - bit_position (int): The bit position within the byte.

        Returns:
        - bool: The boolean value.
        """
        # Extract the byte value from registers using read_reg_val
        byte_value = self.reg_read(address, 0, 0xff)

        # Calculate the boolean value based on the bit position
        return bool((byte_value >> bit_position) & 0x01)
