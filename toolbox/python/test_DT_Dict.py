import unittest


class TestPythonDTDict(unittest.TestCase):

    def test_dictMethods(self):
        dict1 = {'a': 'some value', 'b': [1, 2, 3, 4]}
        self.assertEqual({'a': 'some value', 'b': [1, 2, 3, 4]}, dict1)
        self.assertEqual([1, 2, 3, 4], dict1['b'])

        dict1['c'] = 9                                  #insert new key
        dict1[7] = 'an integer'
        self.assertEqual({'a': 'some value', 'b': [1, 2, 3, 4], 'c': 9, 7: 'an integer'}, dict1)
        self.assertEqual(True, 'b' in dict1)            #check if key exists
        del dict1['a']                                  #delete using key
        self.assertEqual({'b': [1, 2, 3, 4], 'c': 9, 7: 'an integer'}, dict1)
        ret = dict1.pop(7)                              #delete using key and return value
        self.assertEqual({'b': [1, 2, 3, 4], 'c': 9}, dict1)
        self.assertEqual('an integer', ret)

        self.assertEqual(2, len(list(dict1.keys())))    #return iterator of dict keys
        self.assertEqual(2, len(list(dict1.values())))  #return iterator of dict values

        dict2 = {'x': 'another value', 'y': 4}
        dict1.update(dict2)                             #merge one dict into another
        self.assertEqual({'b': [1, 2, 3, 4], 'c': 9, 'x': 'another value', 'y': 4}, dict1)
        dict3 = {'x': 'new value'}
        dict1.update(dict3)                             #merge with override of existing value
        self.assertEqual({'b': [1, 2, 3, 4], 'c': 9, 'x': 'new value', 'y': 4}, dict1)

        self.assertEqual(9, dict1.get('c', 'Tree'))     #use default if key not found
        self.assertEqual('Tree', dict1.get('g', 'Tree'))

    def test_dictFromSequences(self):
        key1 = range(5)
        value1 = reversed(range(5))
        dict1 = dict(zip(key1, value1))                 #create dict from sequences
        self.assertEqual({0: 4, 1: 3, 2: 2, 3: 1, 4: 0}, dict1)
