class ISL94203:

    EEPROM_ADDR_INIT = 0x00
    EEPROM_ADDR_END = 0x4B
    USER_EEPROM_ADDR_INIT = 0x50
    USER_EEPROM_ADDR_END = 0x57
    RAM_ADDR_INIT = 0x80
    RAM_ADDR_END = 0xAB

    NUM_REGISTERS = 5

    def __init__(self):
        self.registers = {}

    def initialize_registers(self, start_address, end_address, initial_value):
        for address in range(start_address, end_address + 1):
            self.registers[address] = initial_value

    def get_register_value(self, address):
        return self.registers.get(address, None)

    def set_register_value(self, address, new_value):
        if address in self.registers:
            self.registers[address] = new_value
            print(f"Register {hex(address)} set to {hex(new_value)}")
        else:
            print(f"Invalid register address: {hex(address)}")

