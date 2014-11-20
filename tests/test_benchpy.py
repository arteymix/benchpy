import unittest

from benchpy import benchmarked

class BenchmarkTestCase(unittest.TestCase):

    def test_decorator(self):
        @benchmarked()
        def foobar():
            pass

        for _ in range(10):
            foobar()

        self.assertEqual(10, len(benchmarked.results[None]['foobar']))

        statistics = benchmarked.statistics()
        self.assertIn(None, statistics)
        self.assertIn('foobar', statistics[None])
        self.assertIn('min', statistics[None]['t'])

    def test_context_manager(self):
        with benchmarked(name='test'):
            pass

        self.assertEqual(1, len(benchmarked.results[None]['test']))

    def test_context_manager_name_missing(self):
        with self.assertRaises(ValueError):
            with benchmarked():
                pass

    def tearDown(self):
        benchmarked.results = {}

if __name__ == '__main__':
    unittest.main()
