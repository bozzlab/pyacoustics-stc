from typing import List, Dict

import plotly.graph_objects as go
import plotly.io as pio

from pyacoustics_stc.constant import (
    STC_CONTOURS,
    FREQUENCY_BAND,
    MAX_DELTA_PER_FREQUENCY,
    MAX_SUM_CONTOUR,
    MAX_DIGIT,
)


FONT = "Open Sans, verdana, arial, sans-serif"
BLACK = "black"


class SoundTransmissionClass:
    def __init__(self, stl: Dict[int, float]):
        self.stl = stl

        self._stc_index: int = None
        self._stc_contour: Dict[int, float] = {}
        self._deficiency: int = None
        self._delta: Dict[int, float] = {}
        self._stl_stc_delta_contours: Dict[int, float] = {}

        self._calculate()

    @property
    def contour(self) -> Dict[int, float]:
        """
        STC contour of STC index.

        example:

        STC index = 20

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
        return self._deficiency

    @property
    def delta(self) -> Dict[int, float]:
        """
        Delta values between STL and STC each frequency.
        """
        return self._delta

    @property
    def index(self) -> int:
        """
        STC index in range 0 -> 149.
        """
        return self._stc_index

    def _plot(self) -> go.Figure:
        y_axis_stl = [value for value in self.stl.values()]
        y_axis_stc = [value for value in self._stc_contour.values()]

        stc_line = go.Scatter(
            x=FREQUENCY_BAND,
            y=y_axis_stc,
            mode="lines+markers",
            marker=dict(color="#FF0000", size=6),
            line=dict(color="#FF0000", width=1, dash="dash"),
            name=f"STC {self.index}",
        )

        stl_line = go.Scatter(
            x=FREQUENCY_BAND,
            y=y_axis_stl,
            mode="lines+markers+text",
            marker=dict(color="#5D69B1", size=6),
            line=dict(color="#0C00FF", width=1),
            name="STL",
        )

        fig = go.Figure()

        fig.add_trace(stc_line)
        fig.add_trace(stl_line)

        fig.update_xaxes(type="log", tickvals=FREQUENCY_BAND, ticktext=FREQUENCY_BAND)
        fig.update_layout(
            title=dict(
                text="Sound Transmission Class (STC) / Sound Transmission Loss (STL)",
                y=0.95,
                x=0.5,
                xanchor="center",
                yanchor="top",
                font=dict(family=FONT, size=25, color=BLACK),
            ),
            xaxis_title=dict(
                text="1/3 Octave Frequency [Hz]",
                font=dict(family=FONT, size=18, color=BLACK),
            ),
            yaxis_title=dict(
                text="(R) Sound Transmission loss [dB]",
                font=dict(family=FONT, size=18, color=BLACK),
            ),
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01,
                font=dict(family=FONT, size=16, color=BLACK),
                bgcolor="#D5EBFF",
                bordercolor=BLACK,
                borderwidth=1,
            ),
        )
        fig.add_annotation(
            x=0.985,
            y=0.025,
            xref="paper",
            yref="paper",
            text="Source: https://github.com/bozzlab/pyacoustics-stc",
            showarrow=False,
            font=dict(family=FONT, size=14, color=BLACK),
            align="center",
            bordercolor=BLACK,
            borderwidth=1,
            borderpad=4,
            bgcolor="#00BDFF",
            opacity=0.8,
        )
        fig.add_annotation(
            x=0.080,
            y=0.9875,
            xref="paper",
            yref="paper",
            text=f"Deficiency {self._deficiency}",
            showarrow=False,
            font=dict(family=FONT, size=14, color=BLACK),
            align="center",
            bordercolor=BLACK,
            borderwidth=1,
            borderpad=4,
            bgcolor="#C9FF00",
            opacity=0.8,
        )

        return fig

    def plot(self):
        fig = self._plot()
        fig.show()

    def export_graph_to_file(self, filename: str, height=1080, width=1920):
        """
        File types supported PNG, JPEG, WebP, SVG and PDF
        https://plotly.com/python/static-image-export/
        """
        fig = self._plot()
        pio.kaleido.scope.default_height = height
        pio.kaleido.scope.default_width = width
        fig.write_image(filename)

    def _calculate(self):
        stl_stc_delta_contours = self._build_stl_stc_delta_contours()
        filtered_delta_contours = self._filter_delta_contours(stl_stc_delta_contours)

        self._stc_index = self._get_stc_index(filtered_delta_contours)
        self._delta = {
            freq: round(value, MAX_DIGIT)
            for freq, value in filtered_delta_contours[self._stc_index].items()
        }
        self._deficiency = round(
            sum(
                [
                    stc_value
                    for stc_value in filtered_delta_contours[self._stc_index].values()
                ]
            ),
            MAX_DIGIT,
        )
        self._stc_contour = STC_CONTOURS[self._stc_index]

    def _build_stl_stc_delta_contours(self) -> Dict[int, float]:
        """
        Building STL and STC delta contours.
        Calculate delta between STL and STC value for each STC index and frequency.

        Structure data of `stl_stc_delta_contours`:

        {
            str_raint (int): {
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

        for _stc_index, stc_contour in STC_CONTOURS.items():
            stl_stc_delta_contours[_stc_index] = {}
            for freq, value in stc_contour.items():
                if self.stl[freq] < value:
                    stl_stc_delta_contours[_stc_index][freq] = abs(
                        self.stl[freq] - value
                    )
                else:
                    stl_stc_delta_contours[_stc_index][freq] = 0

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
            _stc_index: stc_contour
            for _stc_index, stc_contour in stl_stc_delta_contours.items()
            if sum([stc_value for stc_value in stc_contour.values()]) <= MAX_SUM_CONTOUR
        }

        for _stc_index, stc_contour in filtered_sum_delta_contours.items():
            filtered_values = [
                value
                for value in stc_contour.values()
                if value < MAX_DELTA_PER_FREQUENCY
            ]
            if len(filtered_values) == len(FREQUENCY_BAND):
                filtered_delta_contours[_stc_index] = stc_contour

        return filtered_delta_contours

    def _get_stc_index(self, filtered_delta_contours: Dict[int, float]) -> int:
        return max(filtered_delta_contours.keys())
