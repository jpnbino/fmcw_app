from .isl94203_constants import ADDR_USER_EEPROM_OFFSET, ISL94203_EEPROM_SIZE, ISL94203_MEMORY_SIZE, ISL94203_RAM_SIZE, ISL_94203_USER_EEPROM_SIZE, Mask, MAX_ADDRESS
from .isl94203_constants import ADDR_RAM_BEGIN, ADDR_RAM_OFFSET, DEFAULT_CONFIG


class ISL94203_HAL:
    """
    Class representing the ISL94203 battery management system IC. It provides low-level hardware operations to the registers in the ISL94203 following the datasheet. It includes the following operations:
    
    - Set the register values.
    - Get the current register values.
    - Set the RAM values.
    - Get the default configuration values.
    - Get the current configuration values.
    - Write a value to a register based on the specified address, mask, and shift.
    - Read two consecutive registers and extract a value based on the specified bit shift and bit mask.
    - Extract a bit value from the specified address.

    
    **Register Map:**

    - EEPROM: 0x00-0x4B
    - User EEPROM: 0x50-0x57
    - RAM: 0x80-0xAB  

    The register map is then mapped to a continuous array for easy access and serialization.
    """

    def __init__(self):
        """
        Initialize array to represent ISL94203 registers.
        """
        self.all_registers = [0] * ISL94203_MEMORY_SIZE

    def set_registers(self, values: list[int]):
        """
        Set the register values.

        Args:
            values (list[int]): List of values to set in the registers.

        Raises:
            ValueError: If the number of values does not match the number of registers.
        """
        if len(values) != len(self.all_registers):
            raise ValueError(f"Invalid number of values: expected {len(self.all_registers)}, got {len(values)}")
        self.all_registers = values

    def get_registers(self) -> list[int]:
        """
        Get the current register values.

        Returns:
            list[int]: List of current register values.
        """
        return self.all_registers

    @staticmethod
    def get_default_registers() -> list[int]:
        """
        Get the default configuration values as specified in the component's datasheet.

        Returns:
            list[int]: List of default configuration values.
        """
        return DEFAULT_CONFIG

    def set_eeprom_registers(self, values: list[int]):
        """
        Set the EEPROM values of the ISL94203.

        Args:
            values (list[int]): List of values to set in the EEPROM.

        Raises:
            ValueError: If the provided values list is too long.
        """
        if len(values) > ISL94203_EEPROM_SIZE:
            raise ValueError(f"Invalid number of values: expected {ISL94203_EEPROM_SIZE}, got {len(values)}")
        for i, value in enumerate(values):
            self.all_registers[i] = value
    
    def set_user_eeprom_registers(self, values: list[int]):
        """
        Set the User EEPROM values of the ISL94203.

        Args:
            values (list[int]): List of values to set in the User EEPROM.

        Raises:
            ValueError: If the provided values list is too long.
        """
        if len(values) > ISL_94203_USER_EEPROM_SIZE:
            raise ValueError(f"Invalid number of values: expected {ISL_94203_USER_EEPROM_SIZE}, got {len(values)}")
        for i, value in enumerate(values):
            self.all_registers[ADDR_USER_EEPROM_OFFSET + i] = value
            
    def set_ram_registers(self, values: list[int]):
        """
        Set the RAM values of the ISL94203.

        Args:
            values (list[int]): List of values to set in the RAM.

        Raises:
            IndexError: If the provided values list is too long.
        """
        if len(values) > ISL94203_RAM_SIZE:
            raise IndexError(f"Invalid number of values: expected {ISL94203_RAM_SIZE}, got {len(values)}")
        for i, value in enumerate(values):
            self.all_registers[ADDR_RAM_OFFSET + i] = value

    def reg_write(self, address: int, value: int, mask: Mask = Mask.MASK_16BIT, shift: int = 0) -> int:
        """
        Write a value to a register based on the specified address, mask, and shift. Because some values are 16-bit, the function writes to two consecutive registers.

        Args:
            address (int): The address of the register.
            value (int): The value to write to the register.
            mask (Mask, optional): The mask to apply to the value (default is Mask.MASK_16BIT).
            shift (int, optional): The shift to apply to the value (default is 0).

        Returns:
            int: The new value of the register.

        Raises:
            ValueError: If the address or shift is out of valid range.
        """
        if not (0 <= address <= MAX_ADDRESS):
            raise ValueError(f"Invalid register address: {address}")

        if not (0 <= shift <= 15):
            raise ValueError(f"Invalid register shift: {shift}")

        # If the address is in the RAM region, adjust the address to the register index
        if address >= ADDR_RAM_BEGIN:
            address = address - ADDR_RAM_BEGIN + ADDR_RAM_OFFSET

        byte0 = int(self.all_registers[address])
        byte1 = int(self.all_registers[address + 1])

        # Combine the two bytes into a 16-bit value
        tmp = (byte1 << 8) | byte0

        # Clear the bits in the register that correspond to the mask
        tmp &= ~(mask.value << shift)

        # Apply the mask and shift to the new value and combine with the cleared register value
        tmp |= (value & mask.value) << shift

        # Write the result back to the register
        self.all_registers[address] = tmp & 0xff
        self.all_registers[address + 1] = (tmp >> 8) & 0xff

        return tmp


    def reg_read(self, address: int, shift: int = 0, mask: Mask = Mask.MASK_16BIT) -> int:
        """
        Read two consecutive registers and extract a value based on the specified bit shift and bit mask.

        Treats the two bytes as a 16-bit value.

        Args:
            address (int): The starting address of the ISL94203 (0x00-0xA9).
            shift (int, optional): Number of right shifts in value (0-15, default is 0).
            mask (Mask, optional): The bitmask for the value (default is Mask.MASK_16BIT).

        Returns:
            int: Value after applying shift and mask.

        Raises:
            ValueError: If the address or shift is out of valid range.
        """
        if address < 0 or address > 0xA9:
            raise ValueError(f"Invalid address: {address}")

        if shift < 0 or shift > 15:
            raise ValueError(f"Invalid shift: {shift}")

        if address >= ADDR_RAM_BEGIN:
            address = address - ADDR_RAM_BEGIN + ADDR_RAM_OFFSET

        # Assuming start_address points to the index in registers directly
        raw_value = (self.all_registers[address + 1] << 8) | self.all_registers[address]
        value = (raw_value >> shift) & mask.value
        return value

    def reg_write_bit(self, address: int, bit_position: int, value: bool) -> int:
        """
        Write a bit value to a register based on the specified address and bit position.

        Args:
            address (int): The address of the register.
            bit_position (int): The bit position within the byte (0-7).
            value (bool): The boolean value to write.

        Raises:
            ValueError: If the address or bit position is out of valid range.
        """
        self.reg_write(address, value, Mask.MASK_1BIT, bit_position)

    def read_bit(self, address: int, bit_position: int) -> bool:
        """
        Extract a bit value from the specified address. Useful for reading bits like End of Charge(*EOCHG*) at the address *81h*. 

        Args:
            address (int): Real address from ISL94203.
            bit_position (int): The bit position within the byte (0-7).

        Returns:
            bool: The boolean value.

        Raises:
            ValueError: If the address or bit position is out of valid range.
        """
        if address < 0 or address > 0xA9:
            raise ValueError(f"Invalid address: {address}")
        
        if bit_position < 0 or bit_position > 7:
            raise ValueError(f"Invalid bit position: {bit_position}")

        byte_value = self.reg_read(address, 0, Mask.MASK_8BIT)
        
        return bool((byte_value >> bit_position) & 0x01)
    
if __name__ == "__main__":
    # Example usage of the ISL94203 class
    isl94203 = ISL94203_HAL()
    print("ISL94203 HAL initialized.")
    print(f"Memory size (bytes): {ISL94203_MEMORY_SIZE}")

    try:
        # Get and print the default configuration values as in the datasheet
        default_config = ISL94203_HAL.get_default_registers()
        print(f"Default configuration:\n{' '.join(f'{val:02X}' for val in default_config)}")

        # Get and print the current register values
        current_registers = isl94203.get_registers()
        print(f"Current registers:\n{' '.join(f'{val:02X}' for val in current_registers)}")

        # Set EEPROM registers
        eeprom_values = list(range(0, ISL94203_EEPROM_SIZE))
        isl94203.set_eeprom_registers(eeprom_values)
        print("Registers set to default configuration.")

        # Set User EEPROM registers
        user_eeprom_values = list(range(1, ISL_94203_USER_EEPROM_SIZE))
        isl94203.set_user_eeprom_registers(user_eeprom_values)
        print("User EEPROM values set.")

        # Set some RAM values
        ram_values = list(range(1, ISL94203_RAM_SIZE))
        isl94203.set_ram_registers(ram_values)
        print("RAM values set.")

        # Get and print the current configuration values
        current_config = isl94203.get_registers()
        print(f"Current configuration:\n{' '.join(f'{val:02X}' for val in current_config)}")

        # Write a value to a register
        REGISTER_10H = 0x10
        new_value = isl94203.reg_write(REGISTER_10H, 0xABCD)
        print(f"New register value: {new_value:04X}")

        # Read a value from a register
        read_value = isl94203.reg_read(REGISTER_10H)
        print(f"Read register value: {read_value:04X}")

        # Read a bit from a register
        bit_value = isl94203.read_bit(REGISTER_10H, 3)
        print(f"Read bit value: {bit_value}")

    except (ValueError, IndexError) as e:
        print(f"Error: {e}")
