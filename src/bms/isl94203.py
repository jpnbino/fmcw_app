from .constants import MEMORY_SIZE, Mask, MAX_ADDRESS
from .constants import ADDR_RAM_BEGIN, ADDR_RAM_OFFSET, DEFAULT_CONFIG


class ISL94203:
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
        self.registers = [0] * MEMORY_SIZE

    def set_registers(self, values: list[int]):
        """
        Set the register values.

        Args:
            values (list[int]): List of values to set in the registers.

        Raises:
            ValueError: If the number of values does not match the number of registers.
        """
        if len(values) != len(self.registers):
            raise ValueError(f"Invalid number of values: expected {len(self.registers)}, got {len(values)}")
        self.registers = values

    def get_registers(self) -> list[int]:
        """
        Get the current register values.

        Returns:
            list[int]: List of current register values.
        """
        return self.registers

    def set_ram_values(self, values: list[int]):
        """
        Set the RAM values of the ISL94203.

        Args:
            values (list[int]): List of values to set in the RAM.

        Raises:
            IndexError: If the provided values list is too long.
        """
        if len(values) > (len(self.registers) - ADDR_RAM_OFFSET):
            raise IndexError(f"Invalid number of values: expected {len(self.registers) - ADDR_RAM_OFFSET}, got {len(values)}")
        for i, value in enumerate(values):
            self.registers[ADDR_RAM_OFFSET + i] = value

    @staticmethod
    def get_default_config() -> list[int]:
        """
        Get the default configuration values as specified in the component's datasheet.

        Returns:
            list[int]: List of default configuration values.
        """
        return DEFAULT_CONFIG

    def get_config(self) -> list[int]:
        """
        Get the current configuration values.

        Returns:
            list[int]: List of current configuration values.
        """
        return self.registers

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
        raw_value = (self.registers[address + 1] << 8) | self.registers[address]
        value = (raw_value >> shift) & mask.value
        return value

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
    isl94203 = ISL94203()

    # Set some register values
    try:

        print("Registers initialized.")
        print(f"Memory size: {MEMORY_SIZE}")
        print (f"DEFAULT_CONFIG: {len(DEFAULT_CONFIG)}")
    except ValueError as e:
        print(f"Error: {e}")

    # Get and print the current register values
    current_registers = isl94203.get_registers()
    print(f"Current registers: {current_registers}")

    # Set some RAM values
    try:
        isl94203.set_ram_values([0x01, 0x02, 0x03])
        print("RAM values set.")
    except IndexError as e:
        print(f"Error: {e}")

    # Get and print the default configuration values
    default_config = ISL94203.get_default_config()
    print(f"Default configuration: {default_config}")

    # Get and print the current configuration values
    current_config = isl94203.get_config()
    print(f"Current configuration: {current_config}")

    # Write a value to a register
    try:
        new_value = isl94203.reg_write(0x10, 0x1234)
        print(f"New register value: {new_value}")
    except ValueError as e:
        print(f"Error: {e}")

    # Read a value from a register
    try:
        read_value = isl94203.reg_read(0x10)
        print(f"Read register value: {read_value}")
    except ValueError as e:
        print(f"Error: {e}")

    # Read a bit from a register
    try:
        bit_value = isl94203.read_bit(0x10, 3)
        print(f"Read bit value: {bit_value}")
    except ValueError as e:
        print(f"Error: {e}")