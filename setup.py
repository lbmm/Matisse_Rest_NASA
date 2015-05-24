from setuptools import setup, find_packages

import matisseRestNasa

setup(
    name='matisseRestNasa',
    version=matisseRestNasa.__version__,
    author='',
    author_email='',
    packages=find_packages(exclude=['test']),
    description='Matisse ODE Rest Nasa queries',
    long_description=open('README.md').read(),
    url='',
)
