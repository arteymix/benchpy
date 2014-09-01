from setuptools import setup, find_packages

setup(
    name='benchpy',
    version='1.0.0',
    author='Guillaume Poirier-Morency',
    author_email='guillaumepoiriermorency@gmail.com',
    description='Benchmark Python code',
    license='BSD',
    packages=find_packages(),
    requires=['numpy'],
)
