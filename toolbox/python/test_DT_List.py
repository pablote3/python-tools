import unittest


class TestPythonDTList(unittest.TestCase):
    def test_listSlicing(self):
        slice1 = ['a', 'b', 'c']
        self.assertEqual(3, len(slice1))                #length of list
        self.assertEqual('c', slice1[2])
        self.assertEqual('b', slice1[1])
        self.assertEqual('a', slice1[0])
        self.assertEqual('c', slice1[-1])               #last element, slice relative to the end
        self.assertEqual('b', slice1[-2])               #next to last

        self.assertEqual(['a', 'b', 'c'], slice1[0:3])
        self.assertEqual(['b', 'c'], slice1[1:3])
        self.assertEqual(['a', 'b'], slice1[:2])        #from start to 2
        self.assertEqual(['a', 'b', 'c'], slice1[:3])   #from start to 3
        self.assertEqual(['b', 'c'], slice1[1:])        #from 2 to end
        self.assertEqual(['c'], slice1[2:])             #from 3 to end
        self.assertEqual(['a', 'b', 'c'], slice1[:])    #copy entire list

        slice1[1:3] = ['d', 'e']                        #assign using sequence
        self.assertEqual(list(['a', 'd', 'e']), slice1)

    def test_listMethods(self):
        methods1 = ['a', 'b', 'c']
        methods1.append('a')			                #add to end of list
        self.assertEqual(4, len(methods1))
        self.assertEqual('a', methods1[0])
        self.assertEqual('a', methods1[3])
        self.assertEqual('a', methods1[-1])             #last element

        methods1.insert(1, 'red')                       #insert at specific index - slow, move all other indexes
        self.assertEqual('red', methods1[1])
        methods1.pop(1)                                 #remove from specific index - slow, move all other indexes
        self.assertEqual('b', methods1[1])

        self.assertEqual(0, methods1.index('a'))        #find first value
        self.assertEqual(0, methods1.index('a', 0))     #find value with starting index
        self.assertEqual(3, methods1.index('a', 1))
        self.assertEqual(2, methods1.count('a'))        #count number of values
        self.assertEqual(True, 'a' in methods1)         #list contains value - slow, scan entire list
        self.assertEqual(True, 'k' not in methods1)

        methods1[3] = 'z'    				            #replace list element
        self.assertEqual('z', methods1[3])

        methods1.remove('z')                            #removes first instance of value
        self.assertEqual(3, len(methods1))
        self.assertRaises(IndexError, lambda: methods1[3])

        methods1.extend([5, 'b'])                       #add items to existing list
        self.assertEqual(5, len(methods1))

    def test_listSort(self):
        sort1 = ["hello", "1", "True", "-.5"]
        self.assertEqual('hello', sort1[0])
        sort1.sort()                                    #sort existing list alphabetically
        self.assertEqual(list(['-.5', '1', 'True', 'hello']), sort1)
        sort1.sort(key=len)                             #sort existing list by length
        self.assertEqual(list(['1', '-.5', 'True', 'hello']), sort1)

        sort2 = sorted(["hello", "1", "True", "-.5"])   #create sorted list
        self.assertEqual(list(['-.5', '1', 'True', 'hello']), sort2)

        sort3 = reversed(["hello", "1", "True", "-.5"])  #create list in reverse order
        self.assertEqual(list(['-.5', 'True', '1', 'hello']), list(sort3))

    def test_listNumbers(self):
        numbers1 = [3, -5, .6, 17000, 7]
        self.assertEqual(-5, min(numbers1))
        self.assertEqual(17000, max(numbers1))

    def test_listRange(self):
        range1 = range(5)
        self.assertEqual(range(0, 5), range1)
        self.assertEqual([0, 1, 2, 3, 4], list(range1))

    def test_listZip(self):
        list1 = ['foo', 'bar', 'baz']
        list2 = ['one', 'two', 'three']
        zipped1 = zip(list1, list2)                       #pair up elements from two lists
        self.assertEqual([('foo', 'one'), ('bar', 'two'), ('baz', 'three')], list(zipped1))

        list3 = ['one', 'two']
        zipped2 = zip(list1, list3)                       #pair up elements from two lists using shortest sequence
        self.assertEqual([('foo', 'one'), ('bar', 'two')], list(zipped2))

    def test_listFromTuple(self):
        tup1 = ('foo', 'bar', 'baz')
        list1 = list(tup1)
        self.assertEqual(['foo', 'bar', 'baz'], list1)
        list1[1] = 'peep'
        self.assertEqual(['foo', 'peep', 'baz'], list1)

    def test_listComprehension(self):
        list1 = ['a', 'as', 'bat', 'car', 'dove', 'python']
        list2 = [x.upper() for x in list1 if len(x) > 2]    #filter and transform elements
        self.assertEqual(['BAT', 'CAR', 'DOVE', 'PYTHON'], list2)
