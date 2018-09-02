# -*- coding: utf-8 -*-

pytest_plugins = ['helpers_namespace']

import pytest


@pytest.helpers.register
def train_test_cases():
    basic_test_case = [('A', 'a'), ('B', 'b')]

    test_cases = [
    ]

    for i in range(1, 4):
        test_cases.append([basic_test_case] * i)

    # add test case for integer division easily happened in python 2
    test_cases.append(
        [
            [('A', 'a'), ('B', 'b')],
            [('A', 'c'), ('B', 'd')]
        ]
    )

    # return as list of list
    return test_cases
