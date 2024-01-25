import unittest
import myFunc 

class TestTimeFunctions(unittest.TestCase):

    def test_check_time_order(self):
        self.assertTrue(myFunc.check_time_order('10:00 AM', '12:00 PM'))
        self.assertFalse(myFunc.check_time_order('2:00 PM', '11:00 AM'))

    def test_check_is_time_not_between(self):
        self.assertTrue(myFunc.check_is_time_not_between('10:00 AM', '12:00 PM', '9:00 AM', '9:30 AM'))
        self.assertFalse(myFunc.check_is_time_not_between('10:00 AM', '12:00 PM', '11:30 AM', '1:00 PM'))

if __name__ == '__main__':
    unittest.main()