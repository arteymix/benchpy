import numpy
import unittest

from benchpy import benchmarked

class BenchmarkTestCase(unittest.TestCase):

    def test_decorator(self):
        @benchmarked()
        def foobar():
            pass

        for _ in range(10):
            foobar()

        results = benchmarked.results('foobar')
        self.assertIsInstance(results, numpy.ndarray)
        self.assertEqual(10, len(results))

        statistics = benchmarked.statistics('foobar')
        self.assertIn('min', statistics)
        self.assertIsInstance(statistics['min'], numpy.ndarray)

    def test_context_manager(self):
        with benchmarked(name='test'):
            pass

        self.assertEqual(1, len(benchmarked.results('test')))

        results = benchmarked.results('test')
        self.assertIsInstance(results, numpy.ndarray)

        statistics = benchmarked.statistics('test')
        self.assertIn('min', statistics)
        self.assertIsInstance(statistics['min'], numpy.ndarray)

    def test_context_manager_name_missing(self):
        with self.assertRaises(ValueError):
            with benchmarked():
                pass

    def tearDown(self):
        benchmarked._results = {}

if __name__ == '__main__':
    unittest.main()
