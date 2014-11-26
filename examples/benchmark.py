"""
Use benchpy as a full-featured benchmarking utility
"""

from benchpy import benchmarked

l = []

class ListBenchmark:
    def __init__(self):
        self.l = [0]

    @benchmarked()
    def bench_insert(self):
        self.l.insert(0, 5)

b = ListBenchmark()

for _ in range(50000):
    b.bench_insert()

for stat, results in benchmarked.statistics('bench_insert').items():
    print('{} for 50000 insert: {} seconds'.format(stat, results[1]))
