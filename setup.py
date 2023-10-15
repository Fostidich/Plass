import glob

from setuptools import setup, find_packages

setup(
    name='PLASS',
    version='0.1.0',
    packages=find_packages(),
    data_files=[('assets', glob.glob('assets/*'))],
    author='Francesco Ostidich',
    author_email='francesco.ostidich@gmail.com',
    description='A planner for your class lectures',
    url='https://github.com/Fostidich/Plass',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.11',
    ],
)
