from typing import Dict, List

from .constant import FREQUENCY_BAND


def build_frequency_stl_map(transmission_loss: List[float]) -> List[Dict[int, float]]:
    """
    Note: The order of STL value in list must ordered by STC frequency below.

    [125, 160, 200, 250, 315, 400, 500, 630, 800, 1000, 1250, 1600, 2000, 2500, 3150, 4000]

    Input:
        List of Sound Tranmission Loss (STL)
            [
                11.66, 13.3, 14.83, 20.86,
                22.87, 24.94, 26.88, 28.89,
                30.96, 32.9, 34.84, 36.98,
                38.92, 40.86, 27.56, 30.67
            ]

    Output:
        {
            125: 11.66, 160: 13.3, 200: 14.83, 250: 20.86,
            315: 22.87, 400: 24.94, 500: 26.88, 630: 28.89,
            800: 30.96, 1000: 32.9, 1250: 34.84, 1600: 36.98,
            2000: 38.92, 2500: 40.86, 3150: 27.56, 4000: 30.67
        }

    """
    if len(transmission_loss) != len(FREQUENCY_BAND):
        raise ValueError("Length of Transmission Loss invalid")

    return dict(zip(FREQUENCY_BAND, transmission_loss))
