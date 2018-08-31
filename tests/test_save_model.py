#!/bin/env python
# -*- coding: utf-8 -*-

from MicroHMM.hmm import HMMModel


def test_save_model(tmpdir):
    model_dir = tmpdir.mkdir("some_dir")
    model_dir_str = str(model_dir)

    A = {}
    B = {}

    vocabulary = set()

    hmm_model = HMMModel(A, B, vocabulary)
    hmm_model.save_model(model_dir_str)

    assert len(model_dir.listdir()) == 3
