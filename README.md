benchpy
=======

benchpy is a Python utility to benchmark code.

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

Then you can use the `statistics` function to get an overview of the results.
```python
from benchpy import benchmarked

print(benchmarked.results)
print(benchmarked.statistics())
```

Numpy will gratefully comupte the following output
```yaml
group:
    name:
        avg: []
        max: []
        med: []
        min: []
        sum: []
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
