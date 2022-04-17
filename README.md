# pyacoustics-stc
The Python library for Sound Transmission Class (STC) calculation

# Installation
```
pip install pyacoustics-stc
```
## Example
### Calculate STC
```py
from pyacoustics_stc import SoundTransmissionClass

# sound transmission loss as dict object {Frequency : Value}
stl = {
    125: 11.66, 160: 13.303, 200: 14.825, 250: 20.861,
    315: 22.868,400: 24.943, 500: 26.881, 630: 28.889,
    800: 30.964, 1000: 32.902,1250: 34.84,1600: 36.984,
    2000: 38.923, 2500: 40.861, 3150: 27.557, 4000: 30.67,
}

stc = SoundTransmissionClass(stl=stl)

stc.point
# 29
stc.deficiency
# 25.579
stc.contour
# {125: 13, 160: 16, 200: 19, 250: 22, 315: 25, 400: 28, 500: 29, 630: 30, 800: 31, 1000: 32, 1250: 33, 1600: 33, 2000: 33, 2500: 33, 3150: 33, 4000: 33}
stc.delta
# {125: 1.34, 160: 2.697, 200: 4.175, 250: 1.139, 315: 2.132, 400: 3.057, 500: 2.119, 630: 1.111, 800: 0.036, 1000: 0, 1250: 0, 1600: 0, 2000: 0, 2500: 0, 3150: 5.443, 4000: 2.33}

```
### Visualization
```py
stc.plot() # display result as graph
stc.export_graph_result("stc.png") # save graph result as image

# <your_local_path>/stc.png
```
![Sound Transimission Class Graph](https://raw.githubusercontent.com/bozzlab/pyacoustics-stc/main/stc.png)


### Utils 
```py
from pyacoustics_stc.utils import build_frequency_stl_map

stl_without_key = [
    22.49669, 27.85324, 32.77704, 46.30192, 
    52.32415, 58.54912, 64.36372, 70.38595, 
    76.61092, 82.80217, 87.39175, 92.54538, 
    97.27899, 70.36132, 77.44058, 84.8613
]
stl = build_frequency_stl_map(stl_without_key)

stl
# {125: 22.49669, 160: 27.85324, 200: 32.77704, 250: 46.30192, 315: 52.32415, 400: 58.54912, 500: 64.36372, 630: 70.38595, 800: 76.61092, 1000: 82.80217, 1250: 87.39175, 1600: 92.54538, 2000: 97.27899, 2500: 70.36132, 3150: 77.44058, 4000: 84.8613}

```

## Testing
```
python -m pytest
```