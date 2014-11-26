"""
benchpy is an utility for benchmarking Python code.

It defines a decorator and a context manager to benchmark functions and snippets
of code.

Benchmarks results are grouped and named.

@benchmarked(group='foo') # name is defaulted to 'foo'
def foo():
    pass

with benchmarked(group='foo', name='bar'):
    pass
"""
from functools import wraps
import numpy

try:
    from resource import getrusage, RUSAGE_SELF
except ImportError:
    import time
    RUSAGE_SELF = None
    def getrusage(rusage=RUSAGE_SELF):
        """Simulate getrusage from resource module if it's not available"""
        return [(time.time() if i in {0, 1} else 0.0) for i in range(16)]

class benchmarked(object):
    """
    Decorator and context manager for benchmarking functions and snippet of
    code.

    Results are shared amongst instances in _results class attribute.
    """
    _results = {}

    @classmethod
    def results(cls, function, group=None):
        """Returns results for a function in a group"""
        return numpy.array(cls._results[group][function])

    @classmethod
    def statistics(cls, function, group=None):
        """
        Compute statistics (average, max, median, minimun and sum) from _results
        into a numpy array.
        """
        benchmark = cls.results(function, group)
        results = {}
        for name, stat in {'avg': numpy.average, 'max': numpy.amax, 'med': numpy.median, 'min': numpy.amin, 'sum': numpy.sum}.items():
            results[name] = stat(benchmark, axis=0)
        return results

    __slots__ = ['begin', 'group', 'name', 'rusage']

    def __init__(self, group=None, name=None, rusage=RUSAGE_SELF):
        self.begin = None
        self.group = group
        self.name = name
        self.rusage = rusage
        if not group in self._results:
            self._results[group] = {}

    def __call__(self, func):
        """Benchmark a function execution"""
        @wraps(func)
        def wrapper(*args, **kwds):
            """Wraps the function to process a resource delta"""
            if self.name is None:
                self.name = func.__name__

            if self.name not in self._results[self.group]:
                self._results[self.group][self.name] = []

            self.begin = getrusage(self.rusage)

            # actual heavy processing...
            output = func(*args, **kwds)

            # compute a resource usage delta
            delta = tuple(numpy.subtract(getrusage(self.rusage), self.begin))

            # save results
            self._results[self.group][self.name].append(delta)

            return output

        return wrapper

    def __enter__(self):
        if self.name is None:
            raise ValueError('You must set the name parameter to identify the context.')

        if not self in self._results:
            self._results[self.group][self.name] = []

        self.begin = getrusage(self.rusage)

    def __exit__(self, typ, value, traceback):
        # compute a resource usage delta
        delta = tuple(numpy.subtract(getrusage(self.rusage), self.begin))

        # store results
        self._results[self.group][self.name].append(delta)
