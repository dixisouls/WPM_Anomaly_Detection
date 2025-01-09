import os
from utils import timestamp_to_datetime
from config import Config


class DataLogger:
    """
    A class to log WPM data and anomalies to a file.
    """

    def __init__(self, log_dir=Config.LOG_DIR, log_file=Config.LOG_FILE):
        """
        Initialize the DataLogger with a specified log directory and log file.

        Args:
            log_dir (str): The directory where log files will be stored. Defaults to Config.LOG_DIR.
            log_file (str): The name of the log file. Defaults to Config.LOG_FILE.
        """
        self.log_dir = log_dir
        self.log_file = log_file
        self.log_path = os.path.join(log_dir, log_file)

        os.makedirs(log_dir, exist_ok=True)

    def log_data(self, timestamp, wpm, is_anomaly):
        """
        Log WPM data and anomalies to the log file.

        Args:
            timestamp (int): The timestamp in milliseconds.
            wpm (float): The Words Per Minute value.
            is_anomaly (bool): Whether the WPM value is an anomaly.
        """
        dt = timestamp_to_datetime(timestamp)
        log_message = f"[{dt}] WPM: {wpm}"

        if is_anomaly:
            log_message = f"*** {log_message} - ANOMALY DETECTED! ***"

        with open(self.log_path, "a") as f:
            f.write(f"{log_message}\n")

        if is_anomaly:
            print(log_message)
