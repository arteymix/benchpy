from benchpy import benchmarked
import yaml
import time

# example as a context
for i in range(10):
    with benchmarked(name='waiting'):
        time.sleep(0.2)

print(yaml.dump(benchmarked.statistics(), width=1000))
