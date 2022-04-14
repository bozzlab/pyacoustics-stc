from typing import Dict, List


MAX_SUM_CONTOUR: int = 32
MAX_DELTA_PER_FREQUENCY: int = 8
MAX_DIGIT = 5

STC_CONTOURS: Dict[int, Dict[int, float]] = {
    stc_point: {
        125: stc_point - 16,
        160: stc_point - 13,
        200: stc_point - 10,
        250: stc_point - 7,
        315: stc_point - 4,
        400: stc_point - 1,
        500: stc_point + 0,
        630: stc_point + 1,
        800: stc_point + 2,
        1000: stc_point + 3,
        1250: stc_point + 4,
        1600: stc_point + 4,
        2000: stc_point + 4,
        2500: stc_point + 4,
        3150: stc_point + 4,
        4000: stc_point + 4,
    }
    for stc_point in range(150)  # STC range (0 -> 149)
}

FREQUENCY_BAND: List[int] = list(STC_CONTOURS[0].keys())
