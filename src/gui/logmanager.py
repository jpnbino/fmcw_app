from gui.userlog import UserLog

class LogManager:
    def __init__(self):
        self.user_log = None

    def initialize(self, user_log):
        """
        Initialize the LogManager with an existing UserLog instance.
        """
        if isinstance(user_log, UserLog):
            self.user_log = user_log
        else:
            print("Failed to initialize LogManager: Invalid UserLog instance.")
            self.user_log = None

    def log_message(self, message: str):
        """
        Log a message to the UserLog.
        """
        if self.user_log:
            self.user_log.append_message(message)
        else:
            print("LogManager not initialized.")

    def clear_log(self):
        """
        Clear the log in the UserLog.
        """
        if self.user_log:
            self.user_log.clear_log()
        else:
            print("LogManager not initialized. Cannot clear log.")