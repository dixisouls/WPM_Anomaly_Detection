import matplotlib.pyplot as plt
from collections import deque
from utils import timestamp_to_datetime
import matplotlib
import numpy as np
from scipy.interpolate import interp1d

matplotlib.use("Agg")


class DataPlotter:
    """
    A class to plot Words Per Minute (WPM) data over time, with the ability to store and plot data after collection is complete.
    """

    def __init__(self):
        """
        Initialize the DataPlotter with empty deques for timestamps, WPM values, and anomalies,
        and set up the Matplotlib figure and axis.
        """
        self.timestamps = deque()
        self.wpm_values = deque()
        self.anomalies = deque()

        self.fig, self.ax = plt.subplots(figsize=(12, 8))
        (self.line,) = self.ax.plot([], [])
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("WPM")
        self.ax.set_title("Words Per Minute (WPM) Over Time")

    def add_data_point(self, timestamp, wpm, is_anomaly):
        """
        Add a data point to the stored timestamps, WPM values, and anomalies.

        Args:
            timestamp (int): The timestamp of the data point.
            wpm (float): The Words Per Minute (WPM) value of the data point.
            is_anomaly (bool): Whether the data point is an anomaly.
        """
        dt = timestamp_to_datetime(timestamp)
        self.timestamps.append(dt)
        self.wpm_values.append(wpm)
        self.anomalies.append(is_anomaly)

    def plot_and_show(self):
        """
        Plot the collected data, highlight anomalies, and display a smooth interpolated graph.
        """
        # Plot normal data
        normal_x = [
            self.timestamps[i]
            for i in range(len(self.timestamps))
            if not self.anomalies[i]
        ]
        normal_y = [
            self.wpm_values[i]
            for i in range(len(self.wpm_values))
            if not self.anomalies[i]
        ]

        # Check if there is enough data to interpolate
        if len(normal_x) > 1:
            # Convert timestamps to numerical values for interpolation
            x_numeric = [
                dt.timestamp() for dt in normal_x
            ]  # Convert datetime to numeric
            interpolator = interp1d(
                x_numeric, normal_y, kind="cubic"
            )  # Cubic spline interpolation

            # Create a denser set of x values for a smoother curve
            dense_x = np.linspace(min(x_numeric), max(x_numeric), 500)
            dense_y = interpolator(dense_x)  # Interpolated y values

            # Convert back to datetime for plotting
            dense_x_dt = [timestamp_to_datetime(ts) for ts in dense_x]
            self.ax.plot(
                dense_x_dt, dense_y, "b-", label="Smoothed Normal Data"
            )  # Blue smooth line
        else:
            # If no interpolation is possible, plot the normal data as is
            self.ax.plot(normal_x, normal_y, "b-", label="Normal Data")

        # Highlight anomalies (unchanged)
        anomaly_x = [
            self.timestamps[i] for i in range(len(self.timestamps)) if self.anomalies[i]
        ]
        anomaly_y = [
            self.wpm_values[i] for i in range(len(self.wpm_values)) if self.anomalies[i]
        ]
        self.ax.scatter(
            anomaly_x, anomaly_y, color="red", label="Anomaly", zorder=5
        )  # Red points for anomalies

        # Compute the average WPM for the baseline (unchanged)
        if len(self.wpm_values) > 0:
            avg_wpm = sum(self.wpm_values) / len(self.wpm_values)  # Average WPM
            self.ax.axhline(
                y=avg_wpm,
                color="green",
                linestyle="--",
                label=f"Baseline: {avg_wpm:.2f}",
            )

        # Set the tick positions and labels explicitly
        self.ax.set_xticks(
            self.timestamps
        )  # Set tick positions to match the timestamps
        self.ax.set_xticklabels(
            [dt.strftime("%H:%M:%S") for dt in self.timestamps], rotation=45
        )

        # Set plot limits and formatting
        self.ax.relim()
        self.ax.autoscale_view()
        self.ax.legend()

        # Show the plot
        plt.savefig("plot.png")
