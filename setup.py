from distutils.core import setup

setup(
    name='benchpy',
    version='1.0.1',
    author='Guillaume Poirier-Morency',
    author_email='guillaumepoiriermorency@gmail.com',
    url='https://github.com/arteymix/benchpy',
    description='Benchmark Python code',
    download_url='https://github.com/arteymix/benchpy/releases',
    classifiers=['Development Status :: 2 - Pre-Alpha', 'Topic :: System :: Benchmark'],
    packages=['benchpy'],
    requires=['numpy', 'yaml'],
    license='BSD'
)
