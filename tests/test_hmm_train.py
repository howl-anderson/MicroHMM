#!/bin/env python
# -*- coding: utf-8 -*-
import pytest

from MicroHMM.hmm import HMMModel


@pytest.mark.parametrize("train_data", pytest.helpers.train_test_cases())
def test_hmm_train(train_data):
    first_train_data = train_data[0]

    hmm_model = HMMModel()

    for single_train_data in train_data:
        hmm_model.train_one_line(single_train_data)

    hmm_model.do_train()

    result = hmm_model.predict([i[0] for i in first_train_data])

    assert first_train_data == result


def test_hmm_math_error():
    """add test case for integer division easily happened in python 2"""

    hmm_model = HMMModel()
    train_data = [
        [('A', 'a'), ('B', 'b')],
        [('A', 'c'), ('B', 'd')]
    ]

    for single_train_data in train_data:
        hmm_model.train_one_line(single_train_data)

    hmm_model.do_train()
