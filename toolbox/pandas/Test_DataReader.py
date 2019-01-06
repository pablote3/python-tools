import unittest
import pandas as pd
import numpy as np
import os


class TestPandasDataReader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.path = os.path.dirname(__file__) + "/files"

    def test_read_csv(self):
        result = pd.DataFrame([[1, 2, 3, 4, 'hello'], [5, 6, 7, 8, 'world'], [9, 10, 11, 12, 'foo']],
                              index=[0, 1, 2],
                              columns=['a', 'b', 'c', 'd', 'message'])
        df = pd.read_csv(self.path + '/paulHeader.csv')                               #read csv with header
        self.assertTrue(((result == df).all()).all())

        result = pd.DataFrame([[1, 2, 3, 4, 'hello'], [5, 6, 7, 8, 'world'], [9, 10, 11, 12, 'foo']],
                              index=[0, 1, 2],
                              columns=[0, 1, 2, 3, 4])
        df = pd.read_csv(self.path + '/paulNoHeader.csv', header=None)                #read csv without header, default
        self.assertTrue(((result == df).all()).all())

        result = pd.DataFrame([[1, 2, 3, 4, 'hello'], [5, 6, 7, 8, 'world'], [9, 10, 11, 12, 'foo']],
                              index=[0, 1, 2],
                              columns=['a', 'b', 'c', 'd', 'message'])
        df = pd.read_csv(self.path + '/paulNoHeader.csv', names=['a', 'b', 'c', 'd', 'message'])  #specify header names
        self.assertTrue(((result == df).all()).all())

        result = pd.DataFrame([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]],
                              index=['hello', 'world', 'foo'],
                              columns=['a', 'b', 'c', 'd'])
        df = pd.read_csv(self.path + '/paulHeader.csv', index_col='message')          #read csv with header
        self.assertTrue(((result == df).all()).all())

        arrays = [np.array(['one', 'one', 'one', 'one', 'two', 'two', 'two', 'two']),
                  np.array(['a', 'b', 'c', 'd', 'a', 'b', 'c', 'd'])]
        result = pd.DataFrame([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10], [11, 12], [13, 14], [15, 16]],
                              index=arrays,
                              columns=['value1', 'value2'])
        df = pd.read_csv(self.path + '/paulHierarchialIndex.csv', index_col=['key1', 'key2'])  #hierarchial index
        self.assertTrue(((result == df).all()).all())

        result = pd.DataFrame([['one', 1, 2, 3.0, 4, np.nan],
                               ['two', 5, 6, np.nan, 8, 'world'],
                               ['three', 9, 10, 11.0, 12, 'foo']],
                              columns=['something', 'a', 'b', 'c', 'd', 'message'])
        df = pd.read_csv(self.path + '/paulMissingData.csv')                          #read NaN and null
        self.assertTrue(((result == df).any()).all())
        df = pd.read_csv(self.path + '/paulMissingData.csv', na_values=['NULL'])      #set NaN values to null
        self.assertTrue(((result == df).any()).all())

        result = pd.DataFrame([['one', 1, 2, 3.0, 4, np.nan],
                               [np.nan, 5, 6, np.nan, 8, 'world'],
                               ['three', 9, 10, 11.0, 12, np.nan]],
                              columns=['something', 'a', 'b', 'c', 'd', 'message'])
        sentinels = {'message': ['foo', 'NA'], 'something': ['two']}
        df = pd.read_csv(self.path + '/paulMissingData.csv', na_values=sentinels)     #sentinal specified by column
        self.assertTrue(((result == df).any()).all())

        result = pd.DataFrame([[False, False, False, False, False, True],
                               [False, False, False, True, False, False],
                               [False, False, False, False, False, False]],
                              columns=['something', 'a', 'b', 'c', 'd', 'message'])
        df = pd.read_csv(self.path + '/paulMissingData.csv')                          #missing data, isnull
        self.assertTrue(((result == pd.isnull(df)).all()).all())

        df = pd.read_csv(self.path + '/paulHeader.csv', nrows=2)                      #read n number of rows
        self.assertEqual((2, 5), df.shape)

    def test_read_table(self):
        result = pd.DataFrame([[1, 2, 3, 4, 'hello'], [5, 6, 7, 8, 'world'], [9, 10, 11, 12, 'foo']],
                              index=[0, 1, 2],
                              columns=['a', 'b', 'c', 'd', 'message'])
        df = pd.read_table(self.path + '/paulHeader.csv', sep=',')
        self.assertTrue(((result == df).all()).all())

    # def test_read_web(self):
    #     import pandas_datareader.data as web
    #     all_data = {ticker: web.get_data_yahoo(ticker)
    #                 for ticker in ['AAPL', 'IBM', 'MSFT', 'GOOG']
    #              }
    #     price = pd.DataFrame({ticker: data['Adj Close']
    #                           for ticker, data in all_data.items()})
    #     volume = pd.DataFrame({ticker: data['Volume']
    #                            for ticker, data in all_data.items()})
    #
    #     returns = price.pct_change()
    #     series = pd.Series([0.001729, -0.004404, -0.012080, 0.000323], index=['AAPL', 'GOOG', 'IBM', 'MSFT'])
    #     self.assertFalse(((series == returns.iloc[1]).all()).all())
    #
    #     self.assertEqual(0.4727037674161532, returns['MSFT'].corr(returns['IBM']))    #correlation between non-na values
    #     self.assertEqual(7.975231793694253e-05, returns['MSFT'].cov(returns['IBM']))  #covariance between non-na values
    #
    #     series = pd.Series([0.429221, 1.000000, 0.394260, 0.508301], index=['AAPL', 'GOOG', 'IBM', 'MSFT'])
    #     self.assertFalse(((series == returns.corr().iloc[1]).all()).all())            #full correlation
    #     series = pd.Series([0.000103, 0.000230, 0.000071, 0.000109], index=['AAPL', 'GOOG', 'IBM', 'MSFT'])
    #     self.assertFalse(((series == returns.cov().iloc[1]).all()).all())             #full covariance
    #
    #     series = pd.Series([0.361089, 0.394260, 1.000000, 0.472704], index=['AAPL', 'GOOG', 'IBM', 'MSFT'])
    #     self.assertFalse(((series == returns.corrwith(returns.IBM)).all()).all())     #correlation with column
    #     series = pd.Series([-0.066761, -0.017556, -0.162330, -0.087171], index=['AAPL', 'GOOG', 'IBM', 'MSFT'])
    #     self.assertFalse(((series == returns.corrwith(volume)).all()).all())          #correlation with valueLinux333


    def test_read_json(self):
        import json
        obj = """
        {"name": "Wes",
         "places_lived": ["United States", "Spain", "Germany"],
         "pet": null,
         "siblings": [{"name": "Scott", "age": 30, "pets": ["Zues", "Zuko"]},
                      {"name": "Katie", "age": 38, "pets": ["Sixes", "Stache", "Cisco"]}]
        }
        """
        jsn = json.loads(obj)
        siblings = pd.DataFrame(jsn['siblings'], columns=['name', 'age'])
        result = pd.DataFrame([['Scott', 30], ['Katie', 38]], columns=['name', 'age'])
        self.assertTrue(((result == siblings).all()).all())

    def test_write_table(self):
        df = pd.DataFrame([['one', 1, 2, 3.0, 4, np.nan],
                           [np.nan, 5, 6, np.nan, 8, 'world'],
                           ['three', 9, 10, 11.0, 12, np.nan]],
                          columns=['something', 'a', 'b', 'c', 'd', 'message'])
        df.to_csv(self.path + '/comma_del.csv')

        df.to_csv(self.path + '/pipe_del.csv', sep='|')

        df.to_csv(self.path + '/inc_null.csv', na_rep='NULL')

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.path + "/comma_del.csv")
        os.remove(cls.path + "/pipe_del.csv")
        os.remove(cls.path + "/inc_null.csv")
