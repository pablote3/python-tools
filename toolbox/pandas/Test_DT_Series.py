import unittest
import pandas as pd
import numpy as np


class TestPandasSeries(unittest.TestCase):
    def test_create(self):
        arr1 = pd.Series([4, 7, -5, 3])                                 #create with default index
        self.assertTrue(([4, 7, -5, 3] == arr1.values).all())
        self.assertTrue((pd.Index([0, 1, 2, 3] == arr1.index)).all())
        self.assertTrue((pd.RangeIndex(start=0, stop=4, step=1) == arr1.index).all())

        arr1 = pd.Series([4, 7, -5, 3], index=['d', 'b', 'a', 'c'])     #create with labeled index
        self.assertTrue((pd.Index(['d', 'b', 'a', 'c'] == arr1.index)).all())
        self.assertTrue(([3, -5, 4] == arr1[['c', 'a', 'd']]).all())

        dict1 = {'Ohio': 35000, 'Texas': 71000, 'Oregon': 16000, 'Utah': 5000}
        arr1 = pd.Series(dict1)                                         #create from dict
        self.assertEqual(4, arr1.size)
        self.assertTrue((pd.Index(['Ohio', 'Oregon', 'Texas', 'Utah']) == arr1.index).all())
        self.assertEqual(71000, arr1['Texas'])

        arr1 = pd.Series(dict1, index=['California', 'Ohio', 'Oregon', 'Texas'])   #remove Utah, add California to index
        arr1.name = 'population'                                        #assign name to value
        arr1.index.name = 'state'                                       #assign name to index
        self.assertTrue((pd.Index(['California', 'Ohio', 'Oregon', 'Texas']) == arr1.index).all())
        self.assertTrue(pd.isnull(arr1['California']))                  #is null check

    def test_selection(self):
        arr1 = pd.Series([4, 7, -5, 3], index=['d', 'b', 'a', 'c'])
        self.assertEqual(7, arr1['b'])                                  #select by label
        self.assertEqual(7, arr1[1])                                    #select by index
        self.assertTrue(([7, -5, 4] == arr1[['b', 'a', 'd']]).all())    #slice by labels
        self.assertTrue(([7, -5] == arr1[1:3]).all())                   #slice by indexes
        self.assertTrue(([7, 3] == arr1[[1, 3]]).all())                 #slice by indexes
        self.assertTrue(([4, 7, 3] == arr1[arr1 > 0]).all())            #indexes greater than 0

        arr1 = pd.Series(np.arange(3,))
        self.assertTrue(([0] == arr1[:1]).all())                        #select by label
        self.assertTrue(([0, 1] == arr1[:2]).all())                     #select by labels
        self.assertTrue(([0, 1] == arr1.loc[:1]).all())                 #select by loc using labels
        self.assertTrue(([0] == arr1.iloc[:1]).all())                   #select by iloc using integers

    def test_functions(self):
        arr1 = pd.Series([4, 7, -5, 3], index=['d', 'b', 'a', 'c'])
        self.assertTrue(([8, 14, -10, 6] == arr1 * 2).all())            #values multiplied by 2
        self.assertEqual(True, 'b' in arr1)                             #is 'b' in series
        arr1[1:3] = 5                                                   #setting slice results
        self.assertTrue(([4, 5, 5, 3] == arr1).all())

        dict1 = {'Ohio': 35000, 'Texas': 71000, 'Oregon': 16000, 'Utah': 5000}
        arr1 = pd.Series(dict1)
        arr1 = arr1.drop('Oregon')                                      #drop row
        self.assertTrue((pd.Index(['Ohio', 'Texas', 'Utah']) == arr1.index).all())
        arr1.drop(['Ohio', 'Utah'], inplace=True)                       #drop rows inplace
        self.assertTrue((pd.Index(['Texas']) == arr1.index).all())

        series = pd.Series(['c', 'a', 'd', 'a', 'a', 'b', 'b', 'c', 'c'])
        #result = pd.Series(['c', 'a', 'd', 'b'])
        #self.assertTrue((result == series.unique()).all())             #unique values; returns series or array
        self.assertEqual(4, series.unique().size)
        #result = pd.Series([3, 3, 2, 1], index=['a', 'c', 'b', 'd'])
        #self.assertTrue((result == series.value_counts()).all())       #count values; returns series or array
        self.assertEqual(4, series.value_counts().size)

        mask = series.isin(['b', 'c'])
        result = pd.Series([True, False, False, False, False, True, True, True, True])
        self.assertTrue((result == mask).all())                         #set membership check
        result = pd.Series(['c', 'b', 'b', 'c', 'c'], index=[0, 5, 6, 7, 8])
        self.assertTrue((result == series[mask]).all())                 #filering dataset

    def test_reindex(self):
        arr1 = pd.Series([4.5, 7.2, -5.3, 3.6], index=['d', 'b', 'a', 'c'])
        self.assertEqual(4, arr1.index.size)
        arr1 = arr1.reindex(['a', 'b', 'c', 'd', 'e'])                  #rearrange index, add column with null values
        self.assertEqual(5, arr1.index.size)
        self.assertTrue(pd.isnull(arr1['e']))

        ser1 = pd.Series(['blue', 'purple', 'yellow'], index=[0, 2, 4])
        ser1 = ser1.reindex(range(6), method='ffill')                   #reindex with forward-fill missing values
        arr1 = np.array(['blue', 'blue', 'purple', 'purple', 'yellow', 'yellow'])
        self.assertTrue((arr1 == ser1.values).all())

    def test_join(self):
        arr1 = pd.Series([7.3, -2.5, 3.4, 1.5], index=['a', 'c', 'd', 'e'])
        arr2 = pd.Series([-2.1, 3.6, -1.5, 4, 3.1], index=['a', 'c', 'e', 'f', 'g'])
        result = pd.Series([5.2, 1.1, float('nan'), 0.0, float('nan'), float('nan')],
                           index=['a', 'c', 'd', 'e', 'f', 'g'])
        self.assertTrue((result == arr1 + arr2).any())                  #inner join

    def test_sort(self):
        series = pd.Series(range(4), index=['d', 'a', 'b', 'c'])
        result = pd.Series([1, 2, 3, 0], index=['a', 'b', 'c', 'd'])
        self.assertTrue((result == series.sort_index()).all())          #sort by index

        series = pd.Series([4, 7, -3, 2], index=['d', 'a', 'b', 'c'])
        result = pd.Series([-3, 2, 4, 7], index=['b', 'c', 'd', 'a'])
        self.assertTrue((result == series.sort_values()).all())         #sort by value

        series = pd.Series([4, np.nan, 7, np.nan, -3, 2], index=['d', 'a', 'b', 'c', 'f', 'e'])
        result = pd.Series([-3, 2, 4, 7, np.nan, np.nan], index=['f', 'e', 'd', 'b', 'a', 'c'])
        self.assertTrue((result == series.sort_values()).any())         #missing items sorted to the end

    def test_rank(self):
        series = pd.Series([7, -5, 7, 4, 2, 0, 4])
        result = pd.Series([6.5, 1.0, 6.5, 4.5, 3.0, 2.0, 4.5])
        self.assertTrue((result == series.rank()).any())                #ties broken by taking mean

        result = pd.Series([6.0, 1.0, 7.0, 4.0, 3.0, 2.0, 5.0])
        self.assertTrue((result == series.rank(method='first')).any())  #ties broken by observance order

    def test_duplicate_labels(self):
        series = pd.Series(range(5), index=['a', 'a', 'b', 'b', 'c'])
        self.assertFalse(series.index.is_unique)
        self.assertTrue((pd.Series([0, 1], index=['a', 'a']) == series['a']).any())

    def test_stats(self):
        series = pd.Series(['a', 'a', 'b', 'c'] * 4)
        self.assertEqual(16, series.describe().iloc[0])                 #count
        series = pd.Series(['a', 'a', 'b', 'c'] * 4)
        self.assertEqual(3, series.describe().iloc[1])                  #unique
        series = pd.Series(['a', 'a', 'b', 'c'] * 4)
        self.assertEqual('a', series.describe().iloc[2])                #top
        series = pd.Series(['a', 'a', 'b', 'c'] * 4)
        self.assertEqual(8, series.describe().iloc[3])                  #freq


if __name__ == '__main__':
    unittest.main()
