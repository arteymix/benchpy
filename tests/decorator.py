from benchpy import benchmarked

# example as a decorator
@benchmarked()
def factorial(n):
    if n == 0 or n == 1:
        return n
    return n * factorial(n - 1)

print(benchmarked.statistics())
