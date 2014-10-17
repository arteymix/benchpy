import unittest

from benchpy import benchmarked

class BenchmarkTestCase(unittest.TestCase):

    def test_decorator(self):
        @benchmarked()
        def t():
            pass

        for i in range(10):
            t()

        self.assertEquals(10, len(benchmarked.results[None]['t']))

    def test_context_manager(self):
        with benchmarked(name='test'):
            pass

        self.assertEquals(1, len(benchmarked.results[None]['test']))

    def test_context_manager_name_missing(self):
        with self.assertRaises(ValueError):
            with benchmarked():
                pass

    def tearDown(self):
        benchmarked.results = {}

if __name__ == '__main__':
    unittest.main()
