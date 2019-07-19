from setuptools import setup, find_packages

from drf_tree_routers import __version__

with open('flake8-extensions.txt') as f:
    _extra_test_flake8 = [
        line.strip()
        for line in f
    ]
extra_test = [
    'pytest>=4',
    'pytest-cov>=2',
    'pytest-django>=3',
    'psycopg2',

    'flake8',
    *_extra_test_flake8,
]
extra_dev = [
    *extra_test,
]

extra_ci = [
    *extra_test,
    'python-coveralls',
]

setup(
    name='drf-tree-routers',
    version=__version__,
    description='Tree routers for DRF.',

    url='https://github.com/SelfHacked/drf-tree-routers',
    author='SelfDecode',
    author_email='zheng@selfdecode.com',

    packages=find_packages(),

    python_requires='>=3.6',

    install_requires=[
        'django>=2',
        'djangorestframework',
        'returns-decorator',
    ],

    extras_require={
        'test': extra_test,
        'dev': extra_dev,

        'ci': extra_ci,
    },

    classifiers=[
        'Intended Audience :: Developers',

        'Development Status :: 3 - Alpha',

        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',

        'Framework :: Django',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 2.2',

        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
