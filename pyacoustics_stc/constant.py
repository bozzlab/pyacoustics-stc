from typing import Dict, List


MAX_SUM_CONTOUR: int = 32
MAX_DELTA_PER_FREQUENCY: int = 8
MAX_DIGIT = 5

STC_CONTOURS: Dict[int, Dict[int, float]] = {
    stc_index: {
        125: stc_index - 16,
        160: stc_index - 13,
        200: stc_index - 10,
        250: stc_index - 7,
        315: stc_index - 4,
        400: stc_index - 1,
        500: stc_index + 0,
        630: stc_index + 1,
        800: stc_index + 2,
        1000: stc_index + 3,
        1250: stc_index + 4,
        1600: stc_index + 4,
        2000: stc_index + 4,
        2500: stc_index + 4,
        3150: stc_index + 4,
        4000: stc_index + 4,
    }
    for stc_index in range(150)  # STC range (0 -> 149)
}

FREQUENCY_BAND: List[int] = list(STC_CONTOURS[0].keys())
