import unittest


class DataTypeCollections(unittest.TestCase):

    def test_setMethods(self):
        set1 = {2, 2, 2, 1, 3, 3, 4, 5}                 #create set with set keyword
        self.assertEqual({1, 2, 3, 4, 5}, set1)
        set2 = {4, 4, 5, 7, 6, 8, 3, 3}                 #create set with curly braces
        self.assertEqual({3, 4, 5, 6, 7, 8}, set2)

        self.assertEqual({1, 2, 3, 4, 5, 6, 7, 8}, set1.union(set2))    #returns distinct elements from either sets
        self.assertEqual({1, 2, 3, 4, 5, 6, 7, 8}, set1 | set2)
        self.assertEqual({3, 4, 5}, set1.intersection(set2))            #returns elements occurring in both sets
        self.assertEqual({3, 4, 5}, set1 & set2)

        set1.add(6)                                     #add element to set
        self.assertEqual({1, 2, 3, 4, 5, 6}, set1)
        set1.remove(6)                                  #remove element from set
        self.assertEqual({1, 2, 3, 4, 5}, set1)
        set1.pop()                                      #remove arbitrary element from set
        self.assertEqual({2, 3, 4, 5}, set1)

        set2.clear()                                    #reset set to empty
        self.assertEqual(set(), set2)

    def test_setSubset(self):
        set1 = {1, 2, 3, 4, 5}
        self.assertEqual(True, {1, 2, 3}.issubset(set1))
        self.assertEqual(True, set1.issuperset({1, 2, 3}))

    def test_setComprehension(self):
        set1 = {'a', 'as', 'bat', 'car', 'dove', 'python'}
        set2 = {len(x) for x in set1}                   #transform elements
        self.assertEqual({1, 2, 3, 4, 6}, set2)
        set3 = set(map(len, set1))                      #transform elements using map
        self.assertEqual({1, 2, 3, 4, 6}, set3)
