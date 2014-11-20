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
        return [(time.time() if i == 1 else 0.0) for i in range(16)]

class benchmarked(object):
    """
    Decorator and context manager for benchmarking functions and snippet of
    code.
    """
    results = {}

    @classmethod
    def statistics(cls):
        """
        Compute statistics (average, max, median, minimun and sum) from results.
        """
        results = {}
        for group, functions in cls.results.items():
            results[group] = {}
            for function, benchmark in functions:
                function = str(function)
                results[group][function] = {}
                for name, stat in {'avg': numpy.average, 'max': numpy.amax, 'med': numpy.median, 'min': numpy.amin, 'sum': numpy.sum}:
                    results[group][function][name] = float(stat(benchmark, axis=0))
        return results

    def __init__(self, group=None, name=None, rusage=RUSAGE_SELF):
        self.begin = None
        self.group = group
        self.name = name
        self.rusage = rusage
        if not group in self.results:
            self.results[group] = {}

    def __call__(self, func):
        """Benchmark a function execution"""
        @wraps(func)
        def wrapper(*args, **kwds):
            """Wraps the function to process a resource delta"""
            if self.name is None:
                self.name = func.__name__

            if self.name not in self.results[self.group]:
                self.results[self.group][self.name] = []

            self.begin = getrusage(self.rusage)

            # actual heavy processing...
            output = func(*args, **kwds)

            delta = numpy.subtract(getrusage(self.rusage), self.begin)

            # save results
            self.results[self.group][self.name].append(delta)

            return output

        return wrapper

    def __enter__(self):
        if self.name is None:
            raise ValueError('You must set the name parameter to identify the context.')

        if not self in self.results:
            self.results[self.group][self.name] = []

        self.begin = getrusage(self.rusage)

    def __exit__(self, typ, value, traceback):
        delta = numpy.subtract(getrusage(self.rusage), self.begin)
        self.results[self.group][self.name].append(delta)
