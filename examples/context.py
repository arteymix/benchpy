from benchpy import benchmarked
import time

# example as a context
for i in range(10):
    with benchmarked(name='waiting'):
        time.sleep(0.2)

for stat, results in benchmarked.statistics('waiting').items():
    print('{} for waiting: {} seconds in user {} seconds in system'.format(stat, *results))
