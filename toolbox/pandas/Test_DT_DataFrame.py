import unittest
import pandas as pd
import numpy as np


class TestPandasDataFrame(unittest.TestCase):
    def test_create(self):
        dict1 = {'state': ['Ohio', 'Ohio', 'Ohio', 'Nevada', 'Nevada', 'Nevada'],
                 'year': [2000, 2001, 2002, 2001, 2002, 2003],
                 'pop': [1.5, 1.7, 3.6, 2.4, 2.9, 3.2]
                 }
        frame = pd.DataFrame(dict1, columns=['year', 'state', 'pop', 'debt'],   #create from dict
                             index=['one', 'two', 'three', 'four', 'five', 'six'])  #order columns, add debt column
        self.assertTrue((pd.isnull(frame['debt'])).all())                       #retrieve column by label
        self.assertTrue((pd.notnull(frame.year)).all())                         #retrieve column by attribute

        result = pd.Series(['Ohio', 'Ohio', 'Ohio', 'Nevada', 'Nevada', 'Nevada'],
                           index=['one', 'two', 'three', 'four', 'five', 'six'])
        self.assertTrue((result == frame['state']).all())                       #retrieve column as indexed series

        result = pd.Index(['year', 'state', 'pop', 'debt'])
        self.assertTrue((result == frame.loc['three'].index).all())             #retrieve row by position
        result = list([2002, 'Ohio', 3.6, float('nan')])
        self.assertTrue((result == frame.loc['three'].values).any())            #TODO: for all(), casting needed

        debt = pd.Series([-1.2, -1.5, -1.7], index=['two', 'four', 'five'])
        frame['debt'] = debt                                                    #assign list to debt column
        result = list([2001, 'Ohio', 1.7, -1.2])
        self.assertTrue((result == frame.loc['two'].values).any())

        frame['eastern'] = frame.state == 'Ohio'                                #add column of booleans
        self.assertEqual(5, frame.columns.size)
        arr1 = list(['year', 'state', 'pop', 'debt', 'eastern'])
        self.assertTrue((arr1 == frame.columns.values).any())

        frame = pd.DataFrame(np.arange(16).reshape((4, 4)),                     #create with values using arrange
                             index=['Ohio', 'Colorado', 'Utah', 'New York'],
                             columns=['one', 'two', 'three', 'four'])
        self.assertTrue((pd.Index(['one', 'two', 'three', 'four']) == frame.columns).all())
        self.assertTrue((pd.Index(['Ohio', 'Colorado', 'Utah', 'New York']) == frame.index).all())

        dict1 = {'Nevada': {2001: 2.4, 2002: 2.9},                              #create using nested dict
                 'Ohio': {2000: 1.5, 2001: 1.7, 2002: 3.6}
                 }
        frame = pd.DataFrame(dict1)                                             #outer key = columns, inner keys = rows
        self.assertEqual(2, frame.columns.size)
        self.assertEqual(3, frame.index.size)
        self.assertEqual(3, frame.T.columns.size)                               #transpose columns and rows
        self.assertEqual(2, frame.T.index.size)

    def test_selection(self):
        frame = pd.DataFrame(np.arange(16).reshape((4, 4)),                     #create with values using arrange
                             index=['Ohio', 'Colorado', 'Utah', 'New York'],
                             columns=['one', 'two', 'three', 'four'])
        result = pd.Series([1, 5, 9, 13], index=['Ohio', 'Colorado', 'Utah', 'New York'])
        self.assertTrue((result == frame['two']).all())                         #select by column

        result = pd.DataFrame([[2, 0], [6, 4], [10, 8], [14, 12]],
                              index=['Ohio', 'Colorado', 'Utah', 'New York'],
                              columns=['three', 'one'])
        self.assertTrue(((result == frame[['three', 'one']]).all()).all())      #select multiple columns

        result = pd.DataFrame([[0, 1, 2, 3], [4, 5, 6, 7]],
                              index=['Ohio', 'Colorado'],
                              columns=['one', 'two', 'three', 'four'])
        self.assertTrue(((result == frame[:2]).all()).all())                    #select multiple rows

        result = pd.DataFrame([[4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]],
                              index=['Colorado', 'Utah', 'New York'],
                              columns=['one', 'two', 'three', 'four'])
        self.assertTrue(((result == frame[frame['three'] > 5]).all()).all())    #select multiple rows via condition

        result = pd.Series([5, 6], index=['two', 'three'])
        self.assertTrue((result == frame.loc['Colorado', ['two', 'three']]).all())  #select by row and column with loc

        result = pd.Series([1, 5, 9], index=['Ohio', 'Colorado', 'Utah'])
        self.assertTrue((result == frame.loc[:'Utah', 'two']).all())           #select by row and column with iloc

        result = pd.Series([8, 9, 10, 11], index=['one', 'two', 'three', 'four'])
        self.assertTrue((result == frame.iloc[2]).all())                        #select by row with iloc

        result = pd.Series([11, 8, 9], index=['four', 'one', 'two'])
        self.assertTrue((result == frame.iloc[2, [3, 0, 1]]).all())             #select by row and column with iloc

        result = pd.DataFrame([[7, 4, 5], [11, 8, 9]],
                              columns=['four', 'one', 'two'],
                              index=['Colorado', 'Utah'])
        self.assertTrue(((result == frame.iloc[[1, 2], [3, 0, 1]]).all()).all())    #select by row and column with iloc

        result = pd.DataFrame([[4, 5, 6], [8, 9, 10], [12, 13, 14]],
                              columns=['one', 'two', 'three'],
                              index=['Colorado', 'Utah', 'New York'])
        self.assertTrue(((result == frame.iloc[:, :3][frame.three > 5]).all()).all())  #select row, column using where

    def test_dataframe_functions(self):
        frame = pd.DataFrame(np.arange(25).reshape((5, 5)),
                             index=['Ohio', 'Colorado', 'Utah', 'Iowa', 'Texas'],
                             columns=['one', 'two', 'three', 'four', 'five'])

        frame.head()                                                            #select first 5 rows
        frame.tail()                                                            #select last 5 rows

        del frame['five']                                                       #delete column
        self.assertTrue((pd.Index(['one', 'two', 'three', 'four']) == frame.columns).all())
        frame = frame.drop(['Colorado', 'Ohio'])                                #drop rows
        self.assertTrue((pd.Index(['Utah', 'Iowa', 'Texas']) == frame.index).all())
        frame.drop(['two', 'three'], axis='columns', inplace=True)              #drop columns in place
        self.assertTrue((pd.Index(['one', 'four']) == frame.columns).all())

    def test_reindex(self):
        frame = pd.DataFrame(np.arange(9).reshape((3, 3)),
                             index=['a', 'c', 'd'],
                             columns=['Ohio', 'Texas', 'California'])
        self.assertTrue((pd.Index(['a', 'c', 'd']) == frame.index).all())
        self.assertTrue((pd.Index(['Ohio', 'Texas', 'California']) == frame.columns).all())
        result = pd.Series([0., 3., 6.], index=['a', 'c', 'd'])
        self.assertTrue((result == frame['Ohio']).all())
        result = pd.Series([1., 4., 7.], index=['a', 'c', 'd'])
        self.assertTrue((result == frame['Texas']).all())
        result = pd.Series([2., 5., 8.], index=['a', 'c', 'd'])
        self.assertTrue((result == frame['California']).all())

        frame = frame.reindex(['a', 'b', 'c', 'd'])                             #reindex rows
        self.assertTrue((pd.Index(['a', 'b', 'c', 'd']) == frame.index).all())
        self.assertTrue((pd.Index(['Ohio', 'Texas', 'California']) == frame.columns).all())
        result = pd.Series([0., float('nan'), 3., 6.], index=['a', 'b', 'c', 'd'])
        self.assertTrue((result == frame['Ohio']).any())                        #TODO: for all(), casting needed
        result = pd.Series([1., float('nan'), 4., 7.], index=['a', 'b', 'c', 'd'])
        self.assertTrue((result == frame['Texas']).any())
        result = pd.Series([2., float('nan'), 5., 8.], index=['a', 'b', 'c', 'd'])
        self.assertTrue((result == frame['California']).any())

        frame = frame.reindex(columns=['Texas', 'Utah', 'California'])          #reindex columns
        self.assertTrue((pd.Index(['a', 'b', 'c', 'd']) == frame.index).all())
        self.assertTrue((pd.Index(['Texas', 'Utah', 'California']) == frame.columns).all())
        result = pd.Series([1.0, float('nan'), 4.0, 7.0], index=['a', 'b', 'c', 'd'])
        self.assertTrue((result == frame['Texas']).any())

        frame1 = pd.DataFrame(np.arange(12.).reshape((3, 4)), columns=list('abcd'))
        frame2 = pd.DataFrame(np.arange(20.).reshape((4, 5)), columns=list('abcde'))
        frame2.loc[1, 'b'] = np.nan
        frame = frame1.reindex(columns=frame2.columns, fill_value=0)            #reindex columns with fill value
        self.assertTrue((pd.Index(['a', 'b', 'c', 'd', 'e']) == frame.columns).all())
        result = pd.Series([0.0, 1.0, 2.0, 3.0, 0], index=['a', 'b', 'c', 'd', 'e'])
        self.assertTrue(((result == frame.iloc[[0]]).all()).all())
        result = pd.Series([4.0, 5.0, 6.0, 7.0, 0], index=['a', 'b', 'c', 'd', 'e'])
        self.assertTrue(((result == frame.iloc[[1]]).all()).all())

    def test_different_indexes_nan(self):
        frame1 = pd.DataFrame(np.arange(9.).reshape((3, 3)),
                              index=['Ohio', 'Texas', 'Colorado'],
                              columns=list('bcd'))
        frame2 = pd.DataFrame(np.arange(12.).reshape((4, 3)),
                              index=['Utah', 'Ohio', 'Texas', 'Oregon'],
                              columns=list('bde'))
        frame = frame1 + frame2                                                 #inner join
        self.assertTrue((pd.Index(['Colorado', 'Ohio', 'Oregon', 'Texas', 'Utah']) == frame.index).all())
        self.assertTrue((pd.Index(['b', 'c', 'd', 'e']) == frame.columns).all())
        result = pd.Series([3.0, float('nan'), 6.0, float('nan')], index=['b', 'c', 'd', 'e'])
        self.assertTrue(((result == frame.iloc[[1]]).any()).any())
        result = pd.Series([9.0, float('nan'), 12.0, float('nan')], index=['b', 'c', 'd', 'e'])
        self.assertTrue(((result == frame.iloc[[3]]).any()).any())

    def test_different_indexes_fill_values(self):
        frame1 = pd.DataFrame(np.arange(12.).reshape((3, 4)),
                              columns=list('abcd'))
        frame2 = pd.DataFrame(np.arange(20.).reshape((4, 5)),
                              columns=list('abcde'))
        frame2.loc[1, 'b'] = np.nan
        frame = frame1 + frame2                                                 #add with nan values
        self.assertTrue((pd.Index(['a', 'b', 'c', 'd', 'e']) == frame.columns).all())
        result = pd.Series([0.0, 2.0, 4.0, 6.0, np.nan], index=['a', 'b', 'c', 'd', 'e'])
        self.assertTrue(((result == frame.iloc[[0]]).any()).any())
        result = pd.Series([9.0, np.nan, 13.0, 15.0, np.nan], index=['a', 'b', 'c', 'd', 'e'])
        self.assertTrue(((result == frame.iloc[[1]]).any()).any())

        frame = frame1.add(frame2, fill_value=0)                                #add with fill value 0
        self.assertTrue((pd.Index(['a', 'b', 'c', 'd', 'e']) == frame.columns).all())
        result = pd.Series([0.0, 2.0, 4.0, 6.0, 4.0], index=['a', 'b', 'c', 'd', 'e'])
        self.assertTrue(((result == frame.iloc[[0]]).all()).all())
        result = pd.Series([9.0, 5.0, 13.0, 15.0, 9.0], index=['a', 'b', 'c', 'd', 'e'])
        self.assertTrue(((result == frame.iloc[[1]]).all()).all())

    def test_apply_series_operations(self):
        frame = pd.DataFrame(np.arange(12.).reshape((4, 3)),
                             columns=list('bde'),
                             index=['Utah', 'Ohio', 'Texas', 'Oregon'])
        result = pd.Series([0.0, 1.0, 2.0], index=['b', 'd', 'e'])
        self.assertTrue(((result == frame.iloc[[0]]).all()).all())
        result = pd.Series([3.0, 4.0, 5.0], index=['b', 'd', 'e'])
        self.assertTrue(((result == frame.iloc[[1]]).all()).all())

        series = frame.iloc[0]
        frame1 = frame - series                                                 #subtract row 1 from frame
        result = pd.Series([0.0, 0.0, 0.0], index=['b', 'd', 'e'])
        self.assertTrue(((result == frame1.iloc[[0]]).all()).all())
        result = pd.Series([3.0, 3.0, 3.0], index=['b', 'd', 'e'])
        self.assertTrue(((result == frame1.iloc[[1]]).all()).all())

        series = frame['d']
        frame1 = frame.sub(series, axis='index')                                #subtract column d from frame
        result = pd.Series([-1.0, 0.0, 1.0], index=['b', 'd', 'e'])
        self.assertTrue(((result == frame1.iloc[[0]]).all()).all())
        result = pd.Series([-1.0, 0.0, 1.0], index=['b', 'd', 'e'])
        self.assertTrue(((result == frame1.iloc[[1]]).all()).all())

    def test_apply_function(self):
        frame = pd.DataFrame(np.arange(12.).reshape((4, 3)),
                             columns=list('bde'),
                             index=['Utah', 'Ohio', 'Texas', 'Oregon'])
        result = pd.Series([0.0, 1.0, 2.0], index=['b', 'd', 'e'])
        self.assertTrue(((result == frame[0:1]).all()).all())
        result = pd.Series([3.0, 4.0, 5.0], index=['b', 'd', 'e'])
        self.assertTrue(((result == frame[1:2]).all()).all())

        f = lambda x: x.max() + x.min()
        frame1 = frame.apply(f)                                                 #applies function on each column
        result = pd.Series([9.0, 11.0, 13.0], index=['b', 'd', 'e'])
        self.assertTrue((result == frame1).all())

        frame1 = frame.apply(f, axis='columns')                                 #applies function on each row
        result = pd.Series([2.0, 8.0, 14.0, 20.0], index=['Utah', 'Ohio', 'Texas', 'Oregon'])
        self.assertTrue((result == frame1).all())

        f = lambda x: '%.2f'% x
        frame1 = frame.applymap(f)                                              #applymap function to dataFrame
        result = pd.Series(['0.00', '1.00', '2.00'], index=['b', 'd', 'e'])
        self.assertTrue(((result == frame1[0:1]).all()).all())

        series = frame['e'].map(f)                                              #apply function to series
        result = pd.Series(['2.00', '5.00', '8.00', '11.00'], index=['Utah', 'Ohio', 'Texas', 'Oregon'])
        self.assertTrue((result == series).all())

    def test_sort(self):
        frame = pd.DataFrame(np.arange(8).reshape((2, 4)),
                             index=['three', 'one'],
                             columns=['d', 'a', 'b', 'c'])
        frame1 = frame.sort_index()                                              #sort by index on rows
        result = pd.Series([4, 5, 6, 7], index=['d', 'a', 'b', 'c'])
        self.assertTrue(((result == frame1[0:1]).all()).all())
        result = pd.Series([0, 1, 2, 3], index=['d', 'a', 'b', 'c'])
        self.assertTrue(((result == frame1[1:2]).all()).all())

        frame1 = frame.sort_index(axis=1)                                        #sort by index on columns
        result = pd.Series([1, 2, 3, 0], index=['a', 'b', 'c', 'd'])
        self.assertTrue(((result == frame1[0:1]).all()).all())
        result = pd.Series([5, 6, 7, 4], index=['a', 'b', 'c', 'd'])
        self.assertTrue(((result == frame1[1:2]).all()).all())

        frame1 = frame.sort_index(axis=1, ascending=False)                       #sort by index on columns, descending
        result = pd.Series([0, 3, 2, 1], index=['d', 'c', 'b', 'a'])
        self.assertTrue(((result == frame1[0:1]).all()).all())
        result = pd.Series([4, 7, 6, 5], index=['d', 'c', 'b', 'a'])
        self.assertTrue(((result == frame1[1:2]).all()).all())

        frame = pd.DataFrame({'b': [4, 7, -3, 2], 'a': [0, 1, 0, 1]})
        self.assertTrue(((pd.Series([0, 4], index=['a', 'b']) == frame.iloc[[0]]).all()).all())
        self.assertTrue(((pd.Series([1, 7], index=['a', 'b']) == frame.iloc[[1]]).all()).all())
        self.assertTrue(((pd.Series([0, -3], index=['a', 'b']) == frame.iloc[[2]]).all()).all())
        self.assertTrue(((pd.Series([1, 2], index=['a', 'b']) == frame.iloc[[3]]).all()).all())

        frame1 = frame.sort_values(by='b')                                       #sort by single column
        self.assertTrue(((pd.Series([0, -3], index=['a', 'b']) == frame1.iloc[[0]]).all()).all())
        self.assertTrue(((pd.Series([1, 2], index=['a', 'b']) == frame1.iloc[[1]]).all()).all())
        self.assertTrue(((pd.Series([0, 4], index=['a', 'b']) == frame1.iloc[[2]]).all()).all())
        self.assertTrue(((pd.Series([1, 7], index=['a', 'b']) == frame1.iloc[[3]]).all()).all())

        frame1 = frame.sort_values(by=['a', 'b'])                                #sort by multiple columns
        self.assertTrue(((pd.Series([0, -3], index=['a', 'b']) == frame1.iloc[[0]]).all()).all())
        self.assertTrue(((pd.Series([0, 4], index=['a', 'b']) == frame1.iloc[[1]]).all()).all())
        self.assertTrue(((pd.Series([1, 2], index=['a', 'b']) == frame1.iloc[[2]]).all()).all())
        self.assertTrue(((pd.Series([1, 7], index=['a', 'b']) == frame1.iloc[[3]]).all()).all())

    def test_rank(self):
        frame = pd.DataFrame({'b': [4.3, 7, -3, 2], 'a': [0, 1, 0, 1], 'c': [-2, 5, 8, -2.5]})
        frame = frame.rank(axis='columns')
        self.assertTrue(((pd.Series([2.0, 3.0, 1.0], index=['a', 'b', 'c']) == frame.iloc[[0]]).all()).all())
        self.assertTrue(((pd.Series([1.0, 3.0, 2.0], index=['a', 'b', 'c']) == frame.iloc[[1]]).all()).all())
        self.assertTrue(((pd.Series([2.0, 1.0, 3.0], index=['a', 'b', 'c']) == frame.iloc[[2]]).all()).all())
        self.assertTrue(((pd.Series([2.0, 3.0, 1.0], index=['a', 'b', 'c']) == frame.iloc[[3]]).all()).all())

    def test_stats(self):
        frame = pd.DataFrame([[1.4, np.nan], [7.1, -4.5], [np.nan, np.nan], [0.75, -1.3]],
                             index=['a', 'b', 'c', 'd'],
                             columns=['one', 'two'])
        series = pd.Series([9.25, -5.80], index=['one', 'two'])
        self.assertTrue(((series == frame.sum()).all()).all())                   #sum by columns

        series = pd.Series([1.40, 2.60, 0.00, -0.55], index=['a', 'b', 'c', 'd'])
        self.assertTrue(((series == frame.sum(axis='columns')).any()).all())     #sum by columns

        series = pd.Series([np.nan, 1.300, np.nan, -0.275], index=['a', 'b', 'c', 'd'])
        self.assertTrue(((series == frame.mean(axis='columns', skipna=False)).any()).all())   #mean by columns, inc na

        series = pd.Series(['b', 'd'], index=['one', 'two'])
        self.assertTrue(((series == frame.idxmax()).all()).all())                #index of row max values

        series = pd.Series([1.4, np.nan], index=['one', 'two'])
        self.assertTrue(((series == frame.cumsum().iloc[[0]]).any()).any())      #cumulative sum of row values
        series = pd.Series([8.5, -4.5], index=['one', 'two'])
        self.assertTrue(((series == frame.cumsum().iloc[[1]]).all()).all())

        series = pd.Series([3.0, 2.0], index=['one', 'two'])
        self.assertTrue(((series == frame.describe().iloc[[0]]).all()).any())    #count non na values
        series = pd.Series([3.1, -2.9], index=['one', 'two'])
        self.assertTrue(((series == frame.describe().iloc[[1]]).all()).any())    #mean
        series = pd.Series([3.5, 2.3], index=['one', 'two'])
        self.assertFalse(((series == frame.describe().iloc[[2]]).all()).all())   #std
        series = pd.Series([0.75, -4.5], index=['one', 'two'])
        self.assertTrue(((series == frame.describe().iloc[[3]]).all()).all())    #min
        series = pd.Series([1.075, -3.7], index=['one', 'two'])
        self.assertTrue(((series == frame.describe().iloc[[4]]).all()).all())    #25%
        series = pd.Series([1.4, -2.9], index=['one', 'two'])
        self.assertTrue(((series == frame.describe().iloc[[5]]).all()).all())    #50%
        series = pd.Series([4.25, -2.1], index=['one', 'two'])
        self.assertTrue(((series == frame.describe().iloc[[6]]).all()).all())    #75%
        series = pd.Series([7.1, -1.30], index=['one', 'two'])
        self.assertTrue(((series == frame.describe().iloc[[7]]).all()).all())    #max


if __name__ == '__main__':
    unittest.main()
