import unittest
from os import path
import numpy as np

from pymdt import loadmdt
from pymdt import _parse_variable_name
from pymdt import _parse_array_assignment
from pymdt import _parse_is_sub_array_assignment
from pymdt import _parse_sub_array_assignment_index

_TEST_PATH = path.dirname(path.abspath(__file__))

FILE_SIMPLE_M = path.join(_TEST_PATH, 'test_files', 'simple.m')


class TestMDTFile(unittest.TestCase):

    def test_read_simple_m(self):
        d = loadmdt(FILE_SIMPLE_M)

        X = d['X']
        X_should_be = np.array([236227.1094, 241782.6650, 247338.2207])
        np.testing.assert_array_equal(X, X_should_be)

        Y = d['Y']
        Y_should_be = np.array([456467.5000, 462023.0557, 467578.6113])
        np.testing.assert_array_equal(Y, Y_should_be)

        WavelengthCalibr = d['WavelengthCalibr']
        WavelengthCalibr_should_be = np.array([535.9459, 535.9609])
        np.testing.assert_array_equal(WavelengthCalibr, WavelengthCalibr_should_be)

        RamanShiftCalibr = d['RamanShiftCalibr']
        RamanShiftCalibr_should_be = np.array([138.3936, 138.9163])
        np.testing.assert_array_equal(RamanShiftCalibr, RamanShiftCalibr_should_be)

        Map = d['Map']
        Map_should_be = np.array([[[0.0, 1.0], [2.0, 3.0], [4.0, 5.0]], [[6.0, 7.0], [8.0, 9.0], [10.0, 11.0]], [[12.0, 13.0], [14.0, 15.0], [16.0, 17.0]]])
        np.testing.assert_array_almost_equal(Map, Map_should_be)

    def test_parse_variable_name(self):
        line = 'X = [1.0 2.0];'

        var = _parse_variable_name(line)

        self.assertEqual(var, 'X')

        line = 'Map(:,:,1) = [1 2]'
        var = _parse_variable_name(line)
        self.assertEqual(var, 'Map')

    def test_parse_array_assignment_1d(self):
        line = 'Map = [1.0 2.0 3.0 4.0];'

        arr = _parse_array_assignment(line)

        arr_should_be = np.array([1.0, 2.0, 3.0, 4.0])
        np.testing.assert_array_almost_equal(arr, arr_should_be)

    def test_parse_array_assignment_2d(self):
        line = 'Map = [1.0 2.0 ;3.0 4.0 ];'

        arr = _parse_array_assignment(line)

        arr_should_be = np.array([[1.0, 2.0], [3.0, 4.0]])
        np.testing.assert_array_almost_equal(arr, arr_should_be)

    def test_parse_array_assignment_zeros(self):
        line = 'Map = zeros(3,3,2);'

        arr = _parse_array_assignment(line)

        arr_should_be = np.zeros((3,3,2))
        np.testing.assert_array_equal(arr, arr_should_be)

    def test_parse_is_sub_array_assignment(self):
        line = 'Map = zeros(3,3,2);'

        self.assertFalse(_parse_is_sub_array_assignment(line))

        line = 'Map(:,:,1) = [1 2];'

        self.assertTrue(_parse_is_sub_array_assignment(line))

    def test_parse_sub_array_assignment_index(self):
        line = 'Map(:,:,99) = [1 2];'

        index = _parse_sub_array_assignment_index(line)

        self.assertEqual(index, 98)
