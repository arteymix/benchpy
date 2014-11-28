import numpy
import unittest

from benchpy import benchmarked, getrusage, RUSAGE_SELF

class BenchmarkTestCase(unittest.TestCase):

    def test_decorator(self):
        @benchmarked()
        def foobar():
            pass

        for _ in range(10):
            foobar()

        # ensure right internal typing
        self.assertIsInstance(benchmarked._results[None]['foobar'], list)
        self.assertIsInstance(benchmarked._results[None]['foobar'][0], tuple)
        self.assertIsInstance(benchmarked._results[None]['foobar'][0][0], float)

        results = benchmarked.results('foobar')
        self.assertIsInstance(results, numpy.ndarray)
        self.assertEqual(10, len(results))
        self.assertEqual(len(getrusage(RUSAGE_SELF)), len(results[0]))

        statistics = benchmarked.statistics('foobar')
        self.assertIn('min', statistics)
        self.assertIsInstance(statistics['min'], numpy.ndarray)
        self.assertEqual(len(getrusage(RUSAGE_SELF)), len(statistics['min']))

    def test_context_manager(self):
        with benchmarked(name='test'):
            pass

        self.assertIsInstance(benchmarked._results[None]['test'], list)
        self.assertIsInstance(benchmarked._results[None]['test'][0], tuple)


        results = benchmarked.results('test')
        self.assertEqual(1, len(results))
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
