from PySide6.QtWidgets import QStatusBar, QLabel

class StatusBarManager:
    def __init__(self):
        """
        Initialize the StatusBarManager with a QStatusBar instance.

        Args:
            status_bar (QStatusBar): The status bar to manage.
        """
        self.status_bar = None


    def initialize_status_bar_manager(self, status_bar):
        """
        Initialize the global StatusBarManager instance.

        Args:
            status_bar (QStatusBar): The QStatusBar instance to manage.
        """
        if isinstance(status_bar, QStatusBar):
            self.status_bar = status_bar
            print("Status bar initialized.")
        else:
            print("Failed to initialize LogManager: Invalid UserLog instance.")
            self.status_bar = None
            
        # Add persistent widgets (e.g., connection status, logging status)
        self.connection_status_label = QLabel("Disconnected")
        self.connection_status_label.setStyleSheet("color: red;")
        self.status_bar.addPermanentWidget(self.connection_status_label)

        self.logging_status_label = QLabel("Logging: Not started")
        self.logging_status_label.setStyleSheet("color: gray;")
        self.status_bar.addPermanentWidget(self.logging_status_label)

    def update_message(self, message: str, category: str = "info", timeout: int = 5000):
        """
        Update the status bar with a message and optional category.

        Args:
            message (str): The message to display.
            category (str): The category of the message (e.g., "success", "warning", "error", "info").
            timeout (int): The duration (in milliseconds) to display the message (default is 5000ms).
        """
        colors = {
            "success": "green",
            "warning": "orange",
            "error": "red",
            "info": "blue"
        }
        color = colors.get(category, "black")
        self.status_bar.setStyleSheet(f"color: {color};")
        self.status_bar.showMessage(message, timeout)

    def update_connection_status(self, is_connected: bool):
        """
        Update the connection status label.

        Args:
            is_connected (bool): True if connected, False otherwise.
        """
        if is_connected:
            self.connection_status_label.setText("Connected")
            self.connection_status_label.setStyleSheet("color: green;")
        else:
            self.connection_status_label.setText("Disconnected")
            self.connection_status_label.setStyleSheet("color: red;")

    def update_logging_status(self, is_logging: bool):
        """
        Update the logging status label.

        Args:
            is_logging (bool): True if logging is in progress, False otherwise.
        """
        if is_logging:
            self.logging_status_label.setText("Logging: In Progress")
            self.logging_status_label.setStyleSheet("color: green;")
        else:
            self.logging_status_label.setText("Logging: Not started")
            self.logging_status_label.setStyleSheet("color: gray;")
