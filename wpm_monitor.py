import time
from collections import deque
from utils import current_time_ms


class WPMMonitor:
    """
    A class to monitor and calculate Words Per Minute (WPM) over a specified time window.
    """

    def __init__(self, window_size):
        """
        Initialize the WPMMonitor with a specific window size.

        Args:
            window_size (int): The size of the window in seconds for WPM calculation.
        """
        self.window_size = window_size
        self.timestamps = deque()
        self.word_count = 0

    def log_word(self):
        """
        Log a word entry with the current timestamp.
        """
        self.word_count += 1
        self.timestamps.append(current_time_ms())

        # Remove timestamps that are outside the window
        while (current_time_ms() - self.timestamps[0]) / 1000 > self.window_size:
            self.timestamps.popleft()

    def calculate_wpm(self):
        """
        Calculate the Words Per Minute (WPM) based on the logged words and timestamps.

        Returns:
            int: The calculated WPM. Returns 0 if there are not enough timestamps or if the time difference is zero.
        """
        if len(self.timestamps) < 2:
            return 0

        time_diff = (self.timestamps[-1] - self.timestamps[0]) / 1000
        if time_diff <= 0:
            return 0

        # calculate the words typed within the window
        words_in_window = len(self.timestamps)

        wpm = (words_in_window / time_diff) * 60

        return int(wpm)
