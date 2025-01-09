import time
import threading
import sys
import pynput
import matplotlib.pyplot as plt
from wpm_monitor import WPMMonitor
from anomaly_detector import AnomalyDetector
from config import Config
from data_logger import DataLogger
from data_plotter import DataPlotter
from utils import current_time_ms
import argparse


class App:
    """
    Main application class to monitor and log Words Per Minute (WPM) and detect anomalies.
    """

    def __init__(self, algorithm="zscore"):
        """
        Initialize the App with WPMMonitor, AnomalyDetector, DataLogger, and DataPlotter instances.

        Args:
            algorithm (str): The algorithm to use for anomaly detection. Default is "zscore".
        """
        self.monitor = WPMMonitor(window_size=Config.WPM_WINDOW_SIZE)
        self.detector = AnomalyDetector(algorithm=algorithm)
        self.logger = DataLogger()
        self.data_plotter = DataPlotter()
        self.last_log_time = 0
        print(f"\033[1;31m[INFO] - Using {algorithm} algorithm.\033[0m")

    def on_press(self, key):
        """
        Handle key press events to log words.

        Args:
            key (pynput.keyboard.Key): The key that was pressed.
        """
        try:
            if key == pynput.keyboard.Key.space:
                self.monitor.log_word()
        except AttributeError:
            pass

    def on_release(self, key):
        """
        Handle key release events to stop the listener.

        Args:
            key (pynput.keyboard.Key): The key that was released.

        Returns:
            bool: False if the ESC key was released, to stop the listener.
        """
        if key == pynput.keyboard.Key.esc:
            return False

    def log_data_periodically(self):
        """
        Periodically log WPM data and detect anomalies.
        """
        while True:
            current_time = current_time_ms()
            if current_time - self.last_log_time >= Config.LOG_INTERVAL * 1000:
                wpm = self.monitor.calculate_wpm()
                is_anomaly = self.detector.detect_anomaly(wpm)
                self.logger.log_data(current_time, wpm, is_anomaly)
                self.last_log_time = current_time

                self.data_plotter.add_data_point(current_time, wpm, is_anomaly)

            time.sleep(0.1)

    def run(self):
        """
        Start the application, including the logging thread and keyboard listener.
        """
        # start logging thread
        logging_thread = threading.Thread(target=self.log_data_periodically)
        logging_thread.daemon = True
        logging_thread.start()

        # collect all events until released
        with pynput.keyboard.Listener(
            on_press=self.on_press, on_release=self.on_release
        ) as listener:
            print(
                "\033[1;31m[INFO] - Monitoring Started. Press ESC to stop the program.\033[0m"
            )
            listener.join()

        self.data_plotter.plot_and_show()
        print("\033[1;31m[INFO] - Monitoring Stopped. Plot saved to 'plot.png'.\033[0m")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Monitor WPM and detect anomalies.")
    parser.add_argument(
        "--algorithm",
        type=str,
        choices=["zscore", "iqr", "dbscan"],
        required=False,
        default="zscore",
        help="Algorithm to use for anomaly detection. Choices: zscore, iqr, dbscan (case-sensitive). Default is zscore.",
    )

    args = parser.parse_args()

    app = App(algorithm=args.algorithm)
    app.run()
