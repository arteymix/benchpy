from benchpy import benchmarked

@benchmarked(group='factorial')
def factorial_ensemble(n):
    if n in {0, 1}:
        return n
    return n * factorial_ensemble(n - 1)

@benchmarked(group='factorial')
def factorial_one_if(n):
    if n == 0 or n == 1:
        return n
    return n * factorial_one_if(n - 1)

@benchmarked(group='factorial')
def factorial_two_if(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    return n * factorial_two_if(n - 1)

# 1000 iterations
for _ in range(1000):
    factorial_ensemble(50)
    factorial_one_if(50)
    factorial_two_if(50)

for func in {'factorial_ensemble', 'factorial_one_if', 'factorial_two_if'}:
    for stat, results in benchmarked.statistics(func, group='factorial').items():
        print('{} for {}: {} seconds'.format(stat, func, results[1]))
