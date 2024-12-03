from setuptools import setup

setup(
    name='se2121',
    version='0.1',
    py_modules=['cli'],
    install_requires=[
        'Click',
        'requests',
    ],
    entry_points='''
        [console_scripts]
        se2121=cli:cli
    ''',
)
