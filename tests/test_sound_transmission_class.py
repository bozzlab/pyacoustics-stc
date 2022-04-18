import pytest

from pyacoustics_stc import SoundTransmissionClass
from pyacoustics_stc.utils import build_frequency_stl_map
from pyacoustics_stc.constant import FREQUENCY_BAND, STC_CONTOURS


# Input value
stl = {
    125: 11.66,
    160: 13.303,
    200: 14.825,
    250: 20.861,
    315: 22.868,
    400: 24.943,
    500: 26.881,
    630: 28.889,
    800: 30.964,
    1000: 32.902,
    1250: 34.84,
    1600: 36.984,
    2000: 38.923,
    2500: 40.861,
    3150: 27.557,
    4000: 30.67,
}

stl_without_key = [
    22.49669,
    27.85324,
    32.77704,
    46.30192,
    52.32415,
    58.54912,
    64.36372,
    70.38595,
    76.61092,
    82.80217,
    87.39175,
    92.54538,
    97.27899,
    70.36132,
    77.44058,
    84.8613,
]

# Expect value
stc_index = 29
stc_deficiency = 25.579
stc_contour = STC_CONTOURS[stc_index]


@pytest.fixture
def sound_tranmission_class():
    return SoundTransmissionClass(stl=stl)


@pytest.fixture
def frequency_stl_map():
    return build_frequency_stl_map(stl_without_key)


def test_stc_index(sound_tranmission_class):
    assert isinstance(stc_index, int)
    assert stc_index == sound_tranmission_class.index


def test_stc_contour(sound_tranmission_class):
    assert isinstance(stc_contour, dict)
    print(sound_tranmission_class.delta)

    assert stc_contour == sound_tranmission_class.contour


def test_stc_deficiency(sound_tranmission_class):
    assert isinstance(stc_deficiency, float)
    print(sound_tranmission_class.deficiency)
    assert stc_deficiency == sound_tranmission_class.deficiency


def test_build_frequency_stl_map(frequency_stl_map):
    assert isinstance(frequency_stl_map, dict)
    assert FREQUENCY_BAND == list(frequency_stl_map.keys())
