from setuptools import setup

requirements = ['networkx==2.1']
test_requirements = ['pytest==3.5.1']

setup(
    name='MicroHMM',
    version='0.1.1',
    packages=['MicroHMM'],
    url='https://github.com/howl-anderson/MicroHMM',
    install_requires=requirements,
    tests_require=test_requirements,
    license='MIT',
    author='Xiaoquan Kong',
    author_email='u1mail2me@gmail.com',
    description='A micro python package for HMM model'
)
