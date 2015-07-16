# pymdt
[![Build Status](https://travis-ci.org/parkin/pymdt.svg?branch=master)](https://travis-ci.org/parkin/pymdt)

Python package for reading NT-MDT data.

Currently, it reads `.m` maps exported by NT-MDT.

This project is very alpha, and the API is likely to change.

## Usage

```python
from pymdt import loadm

# Load the .m file into a dictionary
d = loadm('exported_map.m')

# Get the Map data
Map = d['Map']

# Get the X and Y axes units of the map itself
X = d['X']
Y = d['Y']

# Get the spectrum at index 1,2
spectrum = Map[1][2]
spectrum_x = X[1] # Corresponding X position

# Get the raman shift (x-axis) for the spectrum data
shift = d['RamanShiftCalibr']

```
