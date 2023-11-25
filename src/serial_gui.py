# serial_gui.py
import tkinter as tk
from tkinter import ttk
from serial.tools import list_ports
from serial_communication import SerialCommunication
from pack_settings import PackSettings

class SerialGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Serial Communication GUI")

        self.create_notebook()
        self.serial_comm = SerialCommunication()
        self.pack_settings = PackSettings(self.tab2)

    def create_notebook(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True)

        self.tab1 = ttk.Frame(self.notebook)
        self.tab2 = ttk.Frame(self.notebook)

        self.notebook.add(self.tab1, text='Serial Configuration')
        self.notebook.add(self.tab2, text='Pack Settings')

        self.create_serial_configuration_widgets()

    def create_serial_configuration_widgets(self):
        self.port_label = ttk.Label(self.tab1, text="Select Serial Port:")
        self.port_label.grid(row=0, column=0, padx=10, pady=10)

        self.port_var = tk.StringVar()
        self.port_combobox = ttk.Combobox(self.tab1, textvariable=self.port_var)
        self.port_combobox.grid(row=0, column=1, padx=10, pady=10)
        self.update_serial_ports()

        self.open_close_button_text = tk.StringVar()
        self.open_close_button_text.set("Open")
        self.open_button = ttk.Button(self.tab1, textvariable=self.open_close_button_text, command=self.toggle_serial)
        self.open_button.grid(row=0, column=2, padx=10, pady=10)

    def update_serial_ports(self):
        ports = [port.device for port in list_ports.comports()]
        self.port_combobox['values'] = ports

    def toggle_serial(self):
        if self.open_close_button_text.get() == "Open":
            self.serial_comm.open_serial(self.port_var.get())
            self.open_close_button_text.set("Close")
        else:
            self.serial_comm.close_serial()
