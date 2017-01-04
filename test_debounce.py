import unittest

import time
from debounce import Debounce



class DebounceBasics(unittest.TestCase):
    def increment(self):
        self.success_count += 1

    def setUp(self):
        self.success_count = 0

    def test_debounce(self):
        # check we started correctly
        self.assertEqual(self.success_count, 0)

        # calls more often than 1.0 seconds will be rejected
        deb = Debounce(1.0)
        deb(self.increment)()
        self.assertEqual(self.success_count, 1)
        deb(self.increment)()
        deb(self.increment)()
        deb(self.increment)()
        deb(self.increment)()
        self.assertEqual(self.success_count, 1)
        self.assertEqual(self.success_count, deb.count)
        time.sleep(1)
        deb(self.increment)()
        self.assertEqual(self.success_count, 2)
        self.assertEqual(self.success_count, deb.count)
        deb.reset()
        deb(self.increment)()
        deb(self.increment)()
        self.assertEqual(self.success_count, 3)
        deb(self.increment)()
        deb(self.increment)()
        self.assertEqual(self.success_count, 3)
        self.assertEqual(self.success_count, deb.count)
        self.assertEqual(deb.count_rejected, 7)


class DebounceLoop(unittest.TestCase):
    def increment(self):
        self.success_count += 1

    def setUp(self):
        self.success_count = 0

    # test that Debounce calls when it's supposed to
    def test_loop(self):
        a = time.time()
        period = 0.2524
        deb = Debounce(period)
        deb(self.increment)()  # call it once to set the debounce timer

        # call it as fast as possible until it goes through
        while True:

            deb(self.increment)()
            if self.success_count != 1:
                b = time.time()
                break

        delta = b-a
        self.assertGreaterEqual(delta, period, "Debounce let a call through before it was supposed to")
        self.assertGreater(deb.count_rejected, 100, "Debounce didn't reject anything")  # this will probably be in the 100 thousands
        self.assertGreater(deb.count_rejected, deb.count, "Debounce let more through than it rejected")
        self.assertEqual(deb.count, 2, "Debounce let more through than it should have")


class DebounceParams(unittest.TestCase):
    def remember(self, input):
        self.memory = input

    def setUp(self):
        self.memory = -1

    def test_debounce(self):
        # check we started correctly
        self.assertEqual(self.memory, -1)

        # calls more often than 1.0 seconds will be rejected
        deb = Debounce(0.1)
        deb(self.remember)(1)
        self.assertEqual(self.memory, 1)
        deb(self.remember)(42)
        self.assertEqual(self.memory, 1)
        deb(self.remember)(90)
        self.assertEqual(self.memory, 1)
        time.sleep(0.1)
        deb(self.remember)(42)
        self.assertEqual(self.memory, 42)
        self.assertEqual(deb.count, 2)

        time.sleep(0.1)
        with self.assertRaises(TypeError):
            deb(self.remember)(43, 43)  # throw for wrong number of params

        self.assertEqual(deb.count, 3, "Throwing an exception did not update counters")

        deb(self.remember)(43)
        self.assertEqual(self.memory, 42, "Throwing an exception did not update last called time")

        time.sleep(0.1)
        with self.assertRaises(TypeError):
            deb(self.remember)()  # throw for wrong number of params


class CustomFnCorrect(unittest.TestCase):
    def increment(self):
        self.success_count += 1

    def goodtime(self):
        return time.time() + 3.14159  # offset doesn't matter

    def setUp(self):
        self.success_count = 0

    def test(self):
        deb = Debounce(0.1)
        deb.time = self.goodtime
        deb(self.increment)()
        self.assertEqual(self.success_count, 1)
        deb(self.increment)()
        deb(self.increment)()
        deb(self.increment)()
        deb(self.increment)()
        self.assertEqual(self.success_count, 1)
        self.assertEqual(self.success_count, deb.count)
        time.sleep(0.1)
        deb(self.increment)()
        self.assertEqual(self.success_count, 2)
        self.assertEqual(self.success_count, deb.count)



class CustomFnWrong(unittest.TestCase):
    def increment(self):
        self.success_count += 1

    def goodtime(self):
        return 0

    def setUp(self):
        self.success_count = 0

    def test(self):
        deb = Debounce(0.1)
        deb.time = self.goodtime
        deb(self.increment)()
        self.assertEqual(self.success_count, 1)
        deb(self.increment)()
        deb(self.increment)()
        deb(self.increment)()
        deb(self.increment)()
        self.assertEqual(self.success_count, 1)
        self.assertEqual(self.success_count, deb.count)
        time.sleep(0.1)
        deb(self.increment)()
        self.assertNotEqual(self.success_count, 2)
        self.assertEqual(self.success_count, deb.count)


if __name__ == '__main__':
    unittest.main()
