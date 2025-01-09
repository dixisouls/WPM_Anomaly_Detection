import numpy as np
from config import Config
from sklearn.cluster import DBSCAN


class AnomalyDetector:
    """
    A class to detect anomalies in Words Per Minute (WPM) data using various algorithms.
    """

    def __init__(self, algorithm="zscore"):
        """
        Initialize the AnomalyDetector with a specified algorithm.

        Args:
            algorithm (str): The anomaly detection algorithm to use. Defaults to "zscore" algorithm.
        """
        self.algorithm = algorithm
        self.data = []

    def detect_anomaly(self, wpm):
        """
        Detect if the given WPM value is an anomaly.

        Args:
            wpm (float): The Words Per Minute value to check for anomalies.

        Returns:
            bool: True if the WPM value is an anomaly, False otherwise.
        """
        self.data.append(wpm)
        if self.algorithm == "zscore":
            return self._zscore_anomaly()
        elif self.algorithm == "iqr":
            return self._iqr_anomaly()
        elif self.algorithm == "dbscan":
            return self._dbscan_anomaly()
        else:
            raise ValueError(f"Invalid anomaly detection algorithm: {self.algorithm}")

    def _zscore_anomaly(self):
        """
        Detect anomalies using the Z-score method.

        Returns:
            bool: True if the latest WPM value is an anomaly based on Z-score, False otherwise.
        """
        if len(self.data) < 2:
            return False

        mean = np.mean(self.data)
        std = np.std(self.data)

        if std == 0:
            return False

        zscore = (self.data[-1] - mean) / std
        return abs(zscore) > Config.ZSCORE_THRESHOLD

    def _iqr_anomaly(self):
        """
        Detect anomalies using the Interquartile Range (IQR) method.

        Returns:
            bool: True if the latest WPM value is an anomaly based on IQR, False otherwise.
        """
        if len(self.data) < 5:
            return False

        q1 = np.percentile(self.data, 25)
        q3 = np.percentile(self.data, 75)
        iqr = q3 - q1
        lower_bound = q1 - Config.IQR_MULTIPLIER * iqr
        upper_bound = q3 + Config.IQR_MULTIPLIER * iqr

        return self.data[-1] < lower_bound or self.data[-1] > upper_bound

    def _dbscan_anomaly(self):
        """
        Detect anomalies using the DBSCAN clustering method.

        Returns:
            bool: True if the latest WPM value is an anomaly based on DBSCAN, False otherwise.
        """
        if len(self.data) < Config.DBSCAN_MIN_SAMPLES:
            return False

        dbscan = DBSCAN(
            eps=Config.DBSCAN_EPSILON, min_samples=Config.DBSCAN_MIN_SAMPLES
        )
        clusters = dbscan.fit_predict(np.array(self.data).reshape(-1, 1))

        # The last data point is considered an anomaly if it is in a cluster of -1
        return clusters[-1] == -1
