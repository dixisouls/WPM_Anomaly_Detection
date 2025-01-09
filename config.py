class Config:
    """
    Configuration class for various parameters used in the application.
    """

    # WPM calculation window size in seconds
    WPM_WINDOW_SIZE = 15

    # Z-score threshold for anomaly detection
    ZSCORE_THRESHOLD = 3.0

    # Interquartile Range (IQR) multiplier for anomaly detection
    IQR_MULTIPLIER = 1.5

    # DBSCAN algorithm parameters
    DBSCAN_EPSILON = 10  # Epsilon parameter for DBSCAN
    DBSCAN_MIN_SAMPLES = 5  # Minimum number of samples for DBSCAN

    # Data logging interval in seconds
    LOG_DIR = "logs"
    LOG_FILE = "wpm_log.log"
    LOG_INTERVAL = 5
