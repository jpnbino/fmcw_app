import tkinter as tk
from tkinter import ttk
import serial
from serial.tools import list_ports

class SerialGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Serial Communication GUI")

        # Create a notebook (tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True)

        # Create tabs
        self.tab1 = ttk.Frame(self.notebook)
        self.tab2 = ttk.Frame(self.notebook)

        self.notebook.add(self.tab1, text='Serial Configuration')
        self.notebook.add(self.tab2, text='Pack Settings')

        # Create a serial object
        self.ser = serial.Serial()

        # Create and place widgets
        self.create_serial_configuration_widgets()
        self.create_pack_settings_widgets()

    def create_serial_configuration_widgets(self):
        # Serial Port Selection
        self.port_label = ttk.Label(self.tab1, text="Select Serial Port:")
        self.port_label.grid(row=0, column=0, padx=10, pady=10)

        self.port_var = tk.StringVar()
        self.port_combobox = ttk.Combobox(self.tab1, textvariable=self.port_var)
        self.port_combobox.grid(row=0, column=1, padx=10, pady=10)
        self.update_serial_ports()

        # Open/Close Serial Button
        self.open_close_button_text = tk.StringVar()
        self.open_close_button_text.set("Open")
        self.open_button = ttk.Button(self.tab1, textvariable=self.open_close_button_text, command=self.toggle_serial)
        self.open_button.grid(row=0, column=2, padx=10, pady=10)

    def create_pack_settings_widgets(self):
        settings_labels = {
            "Voltage Config": [
                "OV Lockout", "Over Voltage", "OV Recover", "End of Charge", "UV Recover",
                "Under Voltage", "Sleep Voltage", "Low V Charge", "UV Lockout", "OV Delay Time",
                "UV Delay Time", "Sleep Volt Delay Time", "Open Wire Sample Time"
            ],
            "Timers": [
                "SLEEP Mode Timer", "WD Timer", "IDLE/DOZE Mode Timer"
            ],
            "Cell Balance": [
                "CB Upper Lim", "CB Lower Lim", "CB Max Delta", "CB Min Delta", "CB Over Temp",
                "CB OT Recover", "CB UT Recover", "CB Under Temp", "CB On Time", "CB Off Time"
            ],
            "Charge/Discharge": [
                "Discharge OC 4mV", "DOC Delay", "Charge OC 1mV", "COC Delay",
                "Discharge SC 16mV", "DSC Delay"
            ],
            "Temperature": [
                "Charge Over Temp", "Charge OT Recover", "Charge UT Recover", "Charge Under Temp",
                "Discharge Over Temp", "Discharge OT Recover", "Discharge UT Recover", "Discharge Under Temp",
                "Internal Over Tmp", "Internal OT Recover"
            ]
        }

        # Create a container frame for the groups
        container_frame = ttk.Frame(self.tab2)
        container_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        row_counter = 1
        col_counter = 0

        for group, labels in settings_labels.items():
            # Create labeled frames for each group
            group_frame = ttk.LabelFrame(container_frame, text=group)
            group_frame.grid(row=row_counter, column=col_counter, padx=10, pady=10, sticky="nsew")
            row_counter += 1

            self.settings_entries = {}
            row = 0
            col = 0

            for label in labels:
                ttk.Label(group_frame, text=label).grid(row=row, column=col, padx=10, pady=5)
                entry = ttk.Entry(group_frame)
                entry.grid(row=row, column=col + 1, padx=10, pady=5)
                self.settings_entries[label] = entry

                row += 1
                if row >= len(labels):
                    row = 0
                    col += 2

            col_counter += 1

        # Buttons to Read/Write Pack Settings
        ttk.Button(container_frame, text="Read Pack Settings", command=self.read_pack_settings).grid(row=row_counter, column=0, padx=10, pady=10)
        ttk.Button(container_frame, text="Write Pack Settings", command=self.write_pack_settings).grid(row=row_counter, column=1, padx=10, pady=10)
        ttk.Button(container_frame, text="Write EEPROM", command=self.write_eeprom).grid(row=row_counter, column=2, padx=10, pady=10)

        # Set row weights for frame resizing
        container_frame.grid_rowconfigure(0, weight=1)

        # Set column weights for frame resizing
        container_frame.grid_columnconfigure(0, weight=1)

    def update_serial_ports(self):
        # Update the list of available serial ports
        ports = [port.device for port in list_ports.comports()]
        self.port_combobox['values'] = ports

    def toggle_serial(self):
        if self.open_close_button_text.get() == "Open":
            self.open_serial()
        else:
            self.close_serial()

    def open_serial(self):
        # Open the selected serial port
        port = self.port_var.get()
        self.ser.port = port
        self.ser.baudrate = 9600  # Adjust the baudrate as needed
        try:
            self.ser.open()
            print(f"Serial port {port} opened\n")
            self.open_close_button_text.set("Close")
        except serial.SerialException as e:
            print(f"Error opening serial port: {e}\n")

    def close_serial(self):
        # Close the serial port
        self.ser.close()
        print(f"Serial port closed\n")
        self.open_close_button_text.set("Open")

    def read_pack_settings(self):
        # Placeholder for reading pack settings from the device
        print("Reading pack settings...\n")

    def write_pack_settings(self):
        # Placeholder for writing pack settings to the device
        print("Writing pack settings...\n")

    def write_eeprom(self):
        # Placeholder for writing to EEPROM
        print("Writing to EEPROM...\n")

# Create the main window
root = tk.Tk()

# Create an instance of the SerialGUI class
app = SerialGUI(root)

# Run the main loop
root.mainloop()
