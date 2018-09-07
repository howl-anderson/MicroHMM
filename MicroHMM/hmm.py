#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import unicode_literals

import math
import pickle
import pathlib
from typing import List, Union, Tuple

from MicroHMM.viterbi import Viterbi


class HMMModel(object):
    # built-in constant
    START_STATE = '<start>'
    END_STATE = '<end>'

    def __init__(self, A=None, B=None, vocabulary=None):
        # only things that Viterbi will used, from training or directly assignment
        self.A = {} if A is None else A
        self.B = {} if B is None else B
        self.vocabulary = set() if vocabulary is None else vocabulary

        # used only for training, temporary variable
        self.state_count = {}  # count of each state
        self.state_bigram = {}  # count of (State_{t} | State_{t-1})
        self.state_observation_pair = {}  # count of pair state and emission observation

    def train_one_line(self, list_of_word_tag_pair):
        # type(List[Union[List[str, str], Tuple[str, str]]) -> None

        """
        train model from one line data
        :param list_of_word_tag_pair: list of tuple (word, tag)
        :return: None
        """
        previous_tag = self.START_STATE
        for word, tag in list_of_word_tag_pair:

            # compute
            # compute transition count
            # compute bigram count
            self._state_bigram_increase_one(previous_tag, tag)

            # compute state count
            self._tag_count_increase_one(previous_tag)

            # update current as previous_tag
            previous_tag = tag

            # compute emission count
            self._state_observation_pair_increase_one(tag, word)

            self.vocabulary.add(word)

        # process last tag
        # NOTE:
        # when program execute to here: previous_tag is last tag, because it was assigned in the end of compute loop
        self._state_bigram_increase_one(previous_tag, self.END_STATE)
        self._tag_count_increase_one(previous_tag)

    def _state_bigram_increase_one(self, previous_tag, tag):
        if previous_tag not in self.state_bigram:
            self.state_bigram[previous_tag] = {}

        tag_state_bigram = self.state_bigram[previous_tag]

        bigram = (previous_tag, tag)

        if bigram not in tag_state_bigram:
            tag_state_bigram[bigram] = 0

        tag_state_bigram[bigram] = tag_state_bigram[bigram] + 1

    def _tag_count_increase_one(self, tag):
        # compute state count
        if tag not in self.state_count:
            self.state_count[tag] = 0

        tag_state_count = self.state_count[tag]

        self.state_count[tag] = tag_state_count + 1

    def do_train(self):
        for previous_state, previous_state_count in self.state_count.items():
            # compute transition probability

            # NOTE: using dict.get() to prevent no such dict key AKA no such bigram pair
            bigram_local_storage = self.state_bigram.get(previous_state, {})
            for bigram, bigram_count in bigram_local_storage.items():
                bigram_probability = bigram_count / previous_state_count

                state = bigram[1]

                if previous_state not in self.A:
                    self.A[previous_state] = {}

                self.A[previous_state][state] = math.log(bigram_probability)

            # compute emission probability
            # NOTE: using dict.get() to prevent start state have on emission will cause exeception
            emission_local_storage = self.state_observation_pair.get(previous_state, {})
            for word, word_count in emission_local_storage.items():
                emmit_probability = word_count / previous_state_count

                if previous_state not in self.B:
                    self.B[previous_state] = {}

                self.B[previous_state][word] = math.log(emmit_probability)

    def predict(self, word_list, output_graphml_file=None):
        # type: (List[str], Union[str, None]) -> List[Tuple[str, str]]

        if not self.A:  # using self.A as an training-flag indicate if already trained.
            self.do_train()

        viterbi = Viterbi(self.A, self.B, self.vocabulary)
        state_list = viterbi.predict_state(word_list)

        if output_graphml_file:
            viterbi.write_graphml(output_graphml_file)

        # remove head and tail tag, AKA start_state and end_state
        tag_list = state_list[1:-1]

        word_tag_pair = zip(word_list, tag_list)

        return list(word_tag_pair)

    def _state_observation_pair_increase_one(self, tag, word):
        if tag not in self.state_observation_pair:
            self.state_observation_pair[tag] = {}

        if word not in self.state_observation_pair[tag]:
            self.state_observation_pair[tag][word] = 0

        self.state_observation_pair[tag][word] = self.state_observation_pair[tag][word] + 1

    def save_model(self, model_dir="model"):
        model_dir_path = pathlib.Path(model_dir)

        self._save_data(self.A, model_dir_path / 'A.pickle')
        self._save_data(self.B, model_dir_path / 'B.pickle')
        self._save_data(self.vocabulary, model_dir_path / 'vocabulary.pickle')

    def _save_data(self, obj, output_file):
        with output_file.open('wb') as fd:
            # using protocol=2 to keep compatible with python 2
            pickle.dump(obj, fd, protocol=2)

    @classmethod
    def load_model(cls, model_dir="model"):
        model_dir_path = pathlib.Path(model_dir)

        A = cls._load_data(model_dir_path / 'A.pickle')
        B = cls._load_data(model_dir_path / 'B.pickle')
        vocabulary = cls._load_data(model_dir_path / 'vocabulary.pickle')

        return cls(A, B, vocabulary)

    @staticmethod
    def _load_data(input_file):
        with input_file.open('rb') as fd:
            obj = pickle.load(fd)
            return obj


if __name__ == "__main__":
    hmm_model = HMMModel()
    hmm_model.train_one_line([("我", "A"), ("是", "B"), ("中国人", "C")])
    hmm_model.train_one_line([("你", "A"), ("去", "B"), ("上海", "C")])
    result = hmm_model.predict(["你", "去", "上海"])
    print(result)
