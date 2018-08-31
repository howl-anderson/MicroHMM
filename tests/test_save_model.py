#!/bin/env python
# -*- coding: utf-8 -*-
import pathlib
from unittest import mock

from MicroHMM.hmm import HMMModel


def test_save_model():
    model_dir = "some_dir"

    A = {}
    B = {}

    vocabulary = set()

    with mock.patch.object(HMMModel, '_save_data',
                           return_value=None) as mock_method:
        hmm_model = HMMModel(A, B, vocabulary)
        hmm_model.save_model(model_dir)

    model_dir_path = pathlib.Path(model_dir)

    mock_method.assert_has_calls([
        mock.call(A, model_dir_path / 'A.json'),
        mock.call(B, model_dir_path / 'B.json'),
        mock.call(vocabulary, model_dir_path / 'vocabulary.json')
    ], any_order=False)
