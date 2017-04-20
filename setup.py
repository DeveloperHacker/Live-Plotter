from setuptools import setup

setup(
    name='live-plotter',
    version='1.0',
    packages=['live_plotter', 'live_plotter.proxy'],
    url='https://github.com/DeveloperHacker/Live-Plotter',
    license='MIT',
    author='HackerMadCat',
    author_email='hacker.mad.cat@gmail.com',
    description='Tiny live plotting library',
    install_requires=[
        'matplotlib',
        'numpy'
    ],
)
