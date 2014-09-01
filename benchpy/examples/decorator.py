from benchpy import benchmarked
import yaml

# example as a decorator
@benchmarked()
def factorial(n):
    if n == 0 or n == 1:
        return n
    return n * factorial(n - 1)

factorial(100)

print(yaml.dump(benchmarked.statistics(), width=1000))
