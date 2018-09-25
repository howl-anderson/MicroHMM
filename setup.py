from setuptools import setup

requirements = ['networkx', 'pathlib;python_version<"3.4"',
                'typing;python_version<"3.5"'
                ]
test_requirements = ['pytest']

setup(
    name='MicroHMM',
    version='0.4.3',
    packages=['MicroHMM'],
    url='https://github.com/howl-anderson/MicroHMM',
    install_requires=requirements,
    tests_require=test_requirements,
    license='MIT',
    author='Xiaoquan Kong',
    author_email='u1mail2me@gmail.com',
    description='A micro python package for HMM model'
)
