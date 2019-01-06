import unittest


class ConditionalStatements(unittest.TestCase):
    def test_if(self):
        self.assertEqual("Greater", condition_if(34, 33))
        self.assertEqual("Equal", condition_if(34, 34))
        self.assertEqual("Less", condition_if(34, 35))

    def test_for(self):
        self.assertEqual(2, condition_for(["apple", "banana", "strawberry", "cherry"]))
        self.assertEqual(3, condition_for(["apple", "banana", None, "cherry"]))
        self.assertEqual(3, condition_for(["apple", "banana", "cherry"]))
        self.assertEqual(2, condition_for(["apple", "banana"]))
        self.assertEqual(1, condition_for(["apple"]))
        self.assertEqual(0, condition_for([]))

    def test_for_enumerate(self):
        self.assertEqual(2, condition_for_enumerate(["apple", "banana", "strawberry", "cherry"]))
        self.assertEqual(3, condition_for_enumerate(["apple", "banana", None, "cherry"]))
        self.assertEqual(2, condition_for_enumerate(["apple", "banana", "cherry"]))
        self.assertEqual(1, condition_for_enumerate(["apple", "banana"]))
        self.assertEqual(0, condition_for_enumerate(["apple"]))
        self.assertRaises(UnboundLocalError, lambda: condition_for_enumerate([]))

    def test_for_range(self):
        self.assertEqual(10, condition_for_range(5))
        self.assertEqual(8, condition_for_range(4))

    def test_while(self):
        self.assertEqual(0, condition_while(5))
        self.assertEqual(1, condition_while(4))
        self.assertEqual(2, condition_while(3))
        self.assertEqual(2, condition_while(2))


if __name__ == '__main__':
    unittest.main()


def condition_if(int1, int2):
    if int1 > int2:
        return "Greater"
    elif int1 < int2:
        return "Less"
    else:
        return "Equal"


def condition_for(fruits):
    i = 0
    for fruit in fruits:
        if fruit is None:
            continue
        elif fruit == "strawberry":
            break
        i += 1
    return i


def condition_for_enumerate(int1):
    for i, fruit in enumerate(int1):
        if fruit is None:
            continue
        elif fruit == "strawberry":
            break
    return i


def condition_for_range(int1):
    i = 0
    for x in range(int1):
        i += 2
    return i


def condition_while(int1):
    i = 0
    while int1 < 5:
        int1 += 1
        i += 1
        if i == 2:
            break
    return i
