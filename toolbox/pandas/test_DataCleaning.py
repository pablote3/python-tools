import unittest
import pandas as pd
import numpy as np


class TestDataCleaning(unittest.TestCase):
    def test_handleMissingData(self):
        arr1 = pd.Series([None, 'artichoke', np.nan, 'avocado'])
        self.assertTrue((pd.Series([True, False, True, False]) == arr1.isnull()).all())
        self.assertTrue((pd.Series([False, True, False, True]) == arr1.notnull()).all())
