import unittest
import re


class Functions(unittest.TestCase):

    def test_parameters(self):
        self.assertEqual("Greater", function_parameters(34, 33))
        self.assertEqual("Greater", function_parameters(34))
        self.assertEqual(None, function_parameters(34, 34))
        self.assertEqual("Less", function_parameters(34, 35))

    def test_multiple_return_values(self):
        self.assertEqual((5, 6, 7), function_multiple_return_values_tuple())
        self.assertEqual({'a': 5, 'b': 6, 'c': 7}, function_multiple_return_values_dict())

    def test_regular_expressions(self):
        strip = lambda x: str.strip(x)                      #remove whitespace
        title = lambda x: str.title(x)                      #camel case
        punctuation = lambda x: re.sub('[!#?]', '', x)      #remove punctuation
        self.assertEqual('Alabama', strip('  Alabama  '))
        self.assertEqual('Georgia', punctuation('?Georgia!'))
        self.assertEqual('Georgia', title('georgia'))
        self.assertEqual('Florida', title('FlOrIda'))
        self.assertEqual('South  Carolina', function_clean_strings('!south  carolina###'))

    def test_lambda(self):
        anon1 = lambda x: x * 2
        self.assertEqual(8, anon1(4))

    def test_generator(self):
        gen1 = function_yield_squares()
        y = []
        for x in gen1:
            y.append(x)
        self.assertEqual([1, 4, 9, 16, 25, 36, 49, 64, 81, 100], y)


if __name__ == '__main__':
    unittest.main()


def function_parameters(positional1, keyword2=1):
    if positional1 > keyword2:
        return "Greater"
    elif positional1 < keyword2:
        return "Less"


def function_multiple_return_values_tuple():
    a = 5
    b = 6
    c = 7
    return a, b, c


def function_multiple_return_values_dict():
    a = 5
    b = 6
    c = 7
    return {'a': a, 'b': b, 'c': c}


def function_clean_strings(value):
    strip = lambda x: str.strip(x)                      #remove whitespace
    title = lambda x: str.title(x)                      #camel case
    punctuation = lambda x: re.sub('[!#?]', '', x)      #remove punctuation
    value = strip(value)
    value = punctuation(value)
    value = title(value)
    return value


def function_yield_squares(n=10):
    for i in range(1, n + 1):
        yield i ** 2
