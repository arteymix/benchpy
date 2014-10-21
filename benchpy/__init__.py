from functools import wraps
import numpy

try:
    raise ImportError
    from resource import getrusage, RUSAGE_SELF
except ImportError:
    import time
    RUSAGE_SELF = None
    def getrusage(rusage=None):
        return 0.0, time.time(), 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0

class benchmarked(object):

    results = {}

    @classmethod
    def statistics(cls):
        results = {}
        for group, functions in cls.results.items():
            results[group] = {}
            for function, benchmark in cls.results[group].items():
                results[group][str(function)] = {
                    'avg': list(map(float, numpy.average(benchmark, axis=0))),
                    'max': list(map(float, numpy.amax(benchmark, axis=0))),
                    'med': list(map(float, numpy.median(benchmark, axis=0))),
                    'min': list(map(float, numpy.amin(benchmark, axis=0))),
                    'sum': list(map(float, numpy.sum(benchmark, axis=0)))
                }
        return results

    def __init__(self, group=None, name=None, rusage=RUSAGE_SELF):
        self.group = group
        self.name = name
        self.rusage = rusage
        if not group in self.results:
            self.results[group] = {}

    def __call__(self, f):
        """ 
        Benchmark a function execution
        """
        @wraps(f)
        def wrapper(*args, **kwds):
            if self.name is None:
                self.name = f.__name__

            if self.name not in self.results[self.group]:
                self.results[self.group][self.name] = []

            self.begin = getrusage(self.rusage)

            # actual heavy processing...
            output = f(*args, **kwds)

            # save results
            self.results[self.group][self.name].append(numpy.subtract(getrusage(self.rusage), self.begin))

            return output

        return wrapper

    def __enter__(self):
        if self.name is None:
            raise ValueError('You must set the name parameter to identify the context.')

        if not self in self.results:
            self.results[self.group][self.name] = []

        self.begin = getrusage(self.rusage)

    def __exit__(self, type, value, traceback):
        self.results[self.group][self.name].append(numpy.subtract(getrusage(self.rusage), self.begin))
