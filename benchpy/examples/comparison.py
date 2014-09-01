from benchpy import benchmarked
import yaml

@benchmarked(group='fibonnaci')
def fibonnaci_ensemble(n):
    if n in {0, 1}:
        return n
    return n * fibonnaci_ensemble(n - 1)

@benchmarked(group='fibonnaci')
def fibonnaci_one_if(n):
    if n == 0 or n == 1:
        return n
    return n * fibonnaci_one_if(n - 1)

@benchmarked(group='fibonnaci')
def fibonnaci_two_if(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    return n * fibonnaci_two_if(n - 1)

# 1000 iterations
for _ in range(1000):
    fibonnaci_ensemble(50)
    fibonnaci_one_if(50)
    fibonnaci_two_if(50)


print(yaml.dump(benchmarked.statistics(), width=1000))
