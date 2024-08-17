from bms.constants import ADDR_RAM_BEGIN, ADDR_RAM_OFFSET, DEFAULT_CONFIG


class ISL94203:
    
    config_values = [0] * len(DEFAULT_CONFIG)

    def __init__(self):
        pass

    # Assuming the values get 16bits, therefore, operations are over two consecutives addresses 
    # example:

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

        byte0 = int(self.config_values[address])
        byte1 = int(self.config_values[address + 1])
        
        # Combine the two bytes into a 16-bit value
        tmp = (byte1 << 8) | byte0

        # Clear the bits in the register that correspond to the mask
        tmp &= ~(mask << shift)

        # Apply the mask and shift to the new value and combine with the cleared register value
        tmp |= (value & mask) << shift

        # Write the result back to the register
        self.config_values[address] = tmp & 0xff
        self.config_values[address + 1] = (tmp >> 8) & 0xff

        return tmp

    def reg_read(self, address, mask=None, shift=0):
        """
        Read a value from a register based on the specified address. 
        If a mask and shift are provided, return the masked and shifted value.
        Otherwise, return the entire register value.

        Parameters:
        - address (int): The address of the register.
        - mask (int, optional): The mask to apply to extract a specific value. Defaults to None.
        - shift (int, optional): The shift to apply after masking. Defaults to 0.

        Returns:
        - int: The entire register value or the extracted value if mask and shift are provided.
        """
        # Read the two bytes from the register
        byte0 = int(self.config_values[address])
        byte1 = int(self.config_values[address + 1])

        # Combine the two bytes into a 16-bit value
        register_value = (byte1 << 8) | byte0

        # If no mask is provided, return the entire register value
        if mask is None:
            return register_value

        # If a mask is provided, apply the mask and shift to extract the desired value
        value = (register_value & mask) >> shift

        return value

    def get_default_config(self):
        return DEFAULT_CONFIG

    def get_config(self):
        return self.config_values