from setuptools import setup

requirements = ['networkx==2.1', 'pathlib;python_version<"3.4"',
                'typing;python_version<"3.5"'
                ]
test_requirements = ['pytest==3.5.1']

setup(
    name='MicroHMM',
    version='0.3.2',
    packages=['MicroHMM'],
    url='https://github.com/howl-anderson/MicroHMM',
    install_requires=requirements,
    tests_require=test_requirements,
    license='MIT',
    author='Xiaoquan Kong',
    author_email='u1mail2me@gmail.com',
    description='A micro python package for HMM model'
)
