import unittest


class ErrorHandling(unittest.TestCase):
    def test_exception_handling(self):
        self.assertEqual(12.25, function_catch_except(12.25))
        self.assertEqual('exception', function_catch_except('three'))
        self.assertEqual('success', function_catch_value_error(12.25))
        self.assertEqual('valueError', function_catch_value_error('three'))


if __name__ == '__main__':
    unittest.main()


def function_catch_except(n=10):
    try:
        return float(n)
    except:
        return 'exception'


def function_catch_value_error(n=10):
    try:
        float(n)
    except ValueError:
        return 'valueError'
    else:
        return 'success'
    finally:
        print()     #dummy event
