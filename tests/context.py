from benchpy import benchmarked

# example as a context
for i in range(10):
    with benchmarked(name='waiting'):
        n = 1000000
        while n:
            n -= 1

print(benchmarked.statistics())
