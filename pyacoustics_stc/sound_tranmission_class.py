from typing import List, Dict

import matplotlib.pylab as plt

from pyacoustics_stc.constant import (
    STC_CONTOURS,
    FREQUENCY_BAND,
    MAX_DELTA_PER_FREQUENCY,
    MAX_SUM_CONTOUR,
    MAX_DIGIT
)


class SoundTransmissionClass:
    def __init__(self, stl: Dict[int, float]):
        self.stl = stl

        self._stc_point: int = None
        self._stc_contour: Dict[int, float] = {}
        self._defiency: int = None
        self._delta: Dict[int, float] = {}
        self._stl_stc_delta_contours: Dict[int, float] = {}

        self._evaluate()

    @property
    def contour(self) -> Dict[int, float]:
        """
        STC contour of STC point.

        example:

        STC Point = 20

        return:
            {
                125: 4, 160: 7, 200: 10, 250: 13,
                315: 16, 400: 19, 500: 20, 630: 21,
                800: 22, 1000: 23, 1250: 24, 1600: 24,
                2000: 24, 2500: 24, 3150: 24, 4000: 24
            }

        """
        return self._stc_contour

    @property
    def deficiency(self) -> float:
        """
        Sum of delta values between STL and STC.
        """
        return self._defiency

    @property
    def delta(self) -> Dict[int, float]:
        """
        Delta values between STL and STC each frequency.
        """
        return self._delta

    @property
    def point(self) -> int:
        """
        STC Point in range 0 -> 149.
        """
        return self._stc_point

    def _plot(self) -> plt:
        x_axis_frequency = []
        x_axis_index = []

        for index, frequency in enumerate(FREQUENCY_BAND):
            x_axis_frequency.append(frequency)
            x_axis_index.append(index)

        y_axis_stl = [value for value in self.stl.values()]
        y_axis_stc = [value for value in self._stc_contour.values()]

        plt.figure(figsize=(18, 8))

        # plot values
        plt.plot(y_axis_stc, "r--", label=f"STC {self._stc_point}")
        plt.plot(y_axis_stl, "b", label="STL")

        # config
        plt.annotate(
            "Source: https://github.com/bozzlab/pyacoustics-stc",
            xy=(0.725, 0.04),
            fontsize=10,
            bbox=dict(facecolor="cyan", alpha=0.5),
            xycoords="axes fraction",
        )
        plt.xticks(x_axis_index, x_axis_frequency, fontsize=12)
        plt.yticks(fontsize=12)
        plt.grid(linestyle="-", linewidth=0.5)
        plt.title("Sound Transmission Class (STC)", fontsize=15, y=1.05)
        plt.legend(loc="upper left")
        plt.xlabel("1/3 Octave Frequency [Hz]", fontsize=15)
        plt.ylabel("(R) Sound Transmission loss [dB]", fontsize=15)

        return plt

    def plot(self):
        plt = self._plot()
        plt.show()

    def export_graph_result(self, filename: str):
        plt = self._plot()
        plt.savefig(f"{filename}")

    def _evaluate(self):
        stl_stc_delta_contours = self._build_stl_stc_delta_contours()
        filtered_delta_contours = self._filter_delta_contours(stl_stc_delta_contours)

        self._stc_point = self._get_stc_point(filtered_delta_contours)
        self._delta = {freq:round(value,MAX_DIGIT) for freq, value in filtered_delta_contours[self._stc_point].items()}
        self._defiency = round(sum(
            [
                stc_value
                for stc_value in filtered_delta_contours[self._stc_point].values()
            ]
        ), MAX_DIGIT)
        self._stc_contour = STC_CONTOURS[self._stc_point]

    def _build_stl_stc_delta_contours(self) -> Dict[int, float]:
        """
        Building STL and STC delta contours.
        Calculate delta between STL and STC value for each STC point and frequency.

        Structure data of `stl_stc_delta_contours`:

        {
            stc_point (int): {
                Freq (int): delta_value (float)
            }
        }

        Example:

        {
            59: {
                125: 17.50,
                160: 7.35,
                ...,
                4000: 0
            },
            60: {
                125: 17.50,
                160: 7.25,
                ...,
                4000: 0
            }
        }

        """
        stl_stc_delta_contours: Dict[int, float] = {}

        for stc_point, stc_contour in STC_CONTOURS.items():
            stl_stc_delta_contours[stc_point] = {}
            for freq, value in stc_contour.items():
                if self.stl[freq] < value:
                    stl_stc_delta_contours[stc_point][freq] = abs(
                        self.stl[freq] - value
                    )
                else:
                    stl_stc_delta_contours[stc_point][freq] = 0

        return stl_stc_delta_contours

    def _filter_delta_contours(
        self, stl_stc_delta_contours: Dict[int, float]
    ) -> Dict[int, float]:
        """
        Filter STC contours are not match with condtions below
        1) Sum delta values for all frequency must less than equal 32 (<= 32)
        2) Delta value each frequency must less than 8 (< 8)
        """
        filtered_delta_contours: Dict[int, float] = {}

        filtered_sum_delta_contours: Dict[int, float] = {
            stc_point: stc_contour
            for stc_point, stc_contour in stl_stc_delta_contours.items()
            if sum([stc_value for stc_value in stc_contour.values()]) <= MAX_SUM_CONTOUR
        }

        for stc_point, stc_contour in filtered_sum_delta_contours.items():
            filtered_values = [
                value
                for value in stc_contour.values()
                if value < MAX_DELTA_PER_FREQUENCY
            ]
            if len(filtered_values) == len(FREQUENCY_BAND):
                filtered_delta_contours[stc_point] = stc_contour

        return filtered_delta_contours

    def _get_stc_point(self, filtered_delta_contours: Dict[int, float]) -> int:
        return max(filtered_delta_contours.keys())
