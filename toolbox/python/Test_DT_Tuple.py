import unittest


class DataTypeCollections(unittest.TestCase):

    def test_tupleSimple(self):
        tup1 = 4, 5, 6, 5
        self.assertEqual((4, 5, 6, 5), tup1)
        self.assertEqual(2, tup1.count(5))              #number of occurrences of a value

    def test_tupleNested(self):
        tup1 = (4, 5, 6), (7, 8)
        self.assertEqual(((4, 5, 6), (7, 8)), tup1)     #nested tuples

    def test_tupleString(self):
        tup1 = tuple('string')
        self.assertEqual(('s', 't', 'r', 'i', 'n', 'g'), tup1)
        self.assertEqual('s', tup1[0])

    def test_tupleConcatenate(self):
        tup1 = (4, None, 'foo') + (6, 0) + ('bar', )
        self.assertEqual((4, None, 'foo', 6, 0, 'bar'), tup1)

    def test_tupleAssignmentUnpacking(self):
        tup1 = (4, 5, 6)
        a, b, c = tup1
        self.assertEqual(4, a)
        self.assertEqual(5, b)
        self.assertEqual(6, c)

    def test_tupleIterateOverSequences(self):
        tup1 = [(1, 2, 3), (4, 5, 6), (7, 8, 9)]
        i = 0
        for a, b, c in tup1:
            if i == 0:
                self.assertEqual(1, a)
                self.assertEqual(2, b)
            elif i == 1:
                self.assertEqual(4, a)
                self.assertEqual(5, b)
            else:
                self.assertEqual(7, a)
                self.assertEqual(8, b)
            i += 1
