from setuptools import find_packages, setup

with open('requirements.in') as f:
    requirements = f.read().splitlines()

setup(
    name='django-import-export-async',
    version='0.1,
    description='Async way to load reports using django-import-export package.',
    author='Vadim Ryazanov',
    license='BSD License',
    packages=find_packages(),
    install_requires=requirements,
)
