from setuptools import setup, find_packages

setup(
    name='MonteCarlo',
    version='1.0.0',
    url='https://github.com/Wilmer-Maldonado/Monte-Carlo.git',
    author='Wilmer Maldonado',
    author_email='etc7fq@virginia.edu',
    description='MonteCarlo Project Module',
    packages=find_packages(),    
    install_requires=['numpy >= 1.11.1', 'matplotlib >= 1.5.1'],
)