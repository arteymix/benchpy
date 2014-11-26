benchpy
=======
benchpy is a Python utility to benchmark code.

Installation
------------
```bash
pip install benchpy
```

Usage
-----
Benchmarks are grouped and named. The default group is `None` and the default
name is the name of the function being benchmarked.

```python
from benchpy import benchmarked

@benchmarked(group='passing', name='')
def function():
  pass
```

You may also benchmark snippet of code using a context manager, in this case,
you must name your benchmark.

```python
from benchpy import benchmarked

with benchmarked(group='passing', name='passing in a context'):
    pass
```

Then you can use the `statistics` function to get an overview of the results of
a given function.
```python
from benchpy import benchmarked

@benchmarked()
def foobar():
    pass

print(benchmarked.results('foobar'))
print(benchmarked.statistics('foobar'))
```

Examples covering basic usage are providen in the
[examples folder](https://github.com/arteymix/benchpy/tree/master/examples).

Results from `results` is stored as a numpy array:
```yaml
[[0.15900000000000003, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
  [0.15900000000000003, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
  [0.15900000000000003, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]]
```

You can then apply any data treatment numpy provides, which is practical for
plotting your results.

The `statistics` function will compute simple statistics about your result set:
```yaml
# [user time, system time, ...]
max: [0.15900000000000003, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
sum: [0.15900000000000003, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
avg: [0.15900000000000003, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
min: [0.15900000000000003, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
med: [0.15900000000000003, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]
```

The fields for each calculation will match those of `resource.getrusage`:
[getrusage documentation](https://docs.python.org/2/library/resource.html#resource.getrusage).

`benchmarked` also allow you to define what kind of `rusage` data you want,
defaulted to `RUSAGE_SELF`.

```python
@benchmarked(rusage=RUSAGE_BOTH)
def foo():
    pass
```

The `resource` module is not available in Windows, so only the second column
will contain relevant information.
