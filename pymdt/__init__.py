from pymdt._version import __version__

import numpy as np
import re


def _parse_variable_name(line):
    """
    :param line: Line in the file
    :returns: The variable name being assigned.

    >>> line = 'X = [1];'
    >>> _parse_variable_name(line)
    X

    """
    rhs = line.split('=')[0].strip()
    if rhs.find('(') >= 0:
        rhs = rhs[:rhs.find('(')]
    return rhs


def _parse_array_assignment(line):
    """
    :param line: String line
    :returns: A numpy array parsed from the line. Works for 1d and 2d arrays.

    >>> line = 'Map = [1 2 3 ;4 5 6];'
    >>> arr = _parse_array_assignment(line)
    >>> arr[0]
    array([1, 2, 3])

    """
    rhs = line.split('=')[1].strip()

    # check to see if there is a zeros function on rhs
    # If so, return a zeros array
    if 'zeros' in rhs:
        shape_str = re.search(r'\((.*)\)', rhs).group(1).strip()
        shape = ()

        for i in shape_str.split(','):
            i = i.strip()
            shape = shape + (int(i),)
        return np.zeros(shape)

    # grab the string between brackets
    arr_str = re.search(r'\[(.*)\]', rhs).group(1).strip()

    # grab the rows
    rows = arr_str.split(';')

    # count the number of rows
    nrows = len(rows)

    first_row = rows[0].strip()

    first_row_cols = first_row.split(' ')

    # count the number of columns
    ncols = len(first_row_cols)

    # initialize the array
    arr = np.zeros((nrows, ncols))

    # fill in the array
    for i, row in enumerate(rows):
        row = row.strip()
        cols = row.split(' ')
        for j, col in enumerate(cols):
            col = col.strip()
            arr[i][j] = float(col)

    # If 1D array, flatten to only one index
    if nrows is 1:
        arr = arr.ravel()

    return arr

def _parse_is_sub_array_assignment(line):
    """
    :param line: String line
    :returns: True if the statment is a sub array assignment. False otherwise.

    >>> line = 'Map(:,:,1) = [1 2 3];'
    >>> _parse_is_sub_array_assignment(line)
    True

    """
    lhs = line.split(' = ')[0].strip()
    if '(' in lhs:
        return True
    return False

def _parse_sub_array_assignment_index(line):
    """
    :param line: String line
    :returns: Index of last dim assigned in assignment

    >>> line = 'Map(:,:,99) = [1 2 3];' # Note that Matlab starts with 1, so 1 is 0th index
    >>> _parse_sub_array_assignment_index(line)
    98

    """
    lhs = line.split(' = ')[0].strip()
    shape_str = re.search(r'\((.*)\)', lhs).group(1).strip()

    return int(shape_str.split(',')[2]) - 1

def loadm(filename):
    """
    Loads an area scan .m file, exported by NT-MDT, into a dictionary.

    :param filename: Filename of (path to) .m file
    :returns: A dictionary containing what the result would be if the NT-MDT .m
                script was run in Matlab.

    >>> d = loadm('pymdt/tests/test_files/simple.m')

    `d` Will then have the following contents:

        {
            'X': 1D numpy array of x position values in Angstroms,
            'Y': 1D numpy array of y position values in Angstroms,
            'WavelengthCalibr': 1D array of wavelengths in nm corresponing to
                the x-axis for the spectra at each pixel,
            'RamanShiftCalibr': 1D array of Raman shifts in 1/cm corresponing to
                the x-axis for the spectra at each pixel,
            'Map': 2D spectra map. Map[1][2][:] would return the spectrum at
                position X[1], Y[2]
        }
    """
    result = {}

    with open(filename, 'r') as f:
        for line in f:
            if len(line.strip()) > 1:
                var_name = _parse_variable_name(line)
                arr = _parse_array_assignment(line)
                if _parse_is_sub_array_assignment(line):
                    index = _parse_sub_array_assignment_index(line)
                    result[var_name][:,:,index] = arr
                else:
                    result[var_name] = arr

    return result
