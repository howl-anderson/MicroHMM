# -*- coding: utf-8 -*-
import math

import networkx as nx


class MockedGraph:
    def do_nothing(self, *args, **kwargs):
        pass

    add_node = do_nothing
    add_edge = do_nothing


class Viterbi(object):
    def __init__(self, A, B, vocabulary, start_state='<start>', end_state='<end>', very_small_probability=1e-32, store_graph=False):
        self.A = A
        self.B = B
        self.vocabulary = vocabulary

        self.start_state = start_state
        self.end_state = end_state

        self.trellis = {}

        # Trk part for robust model
        # TODO: why using a very small number than average_emission_probability can archive better performance?
        self.very_small_probability = math.log(very_small_probability)

        # create networkx graph
        self.G = nx.Graph() if store_graph else MockedGraph()

    def _do_predict(self, word_list):
        N = len(word_list)
        T = N - 1
        trackback = {}

        all_states = set(self.A.keys()) - {self.start_state}  # remove start_state

        # initialization step
        self.G.add_node(self.start_state)

        word = word_list[0]
        for state in all_states:

            self.trellis[state] = {}

            # NOTE: this is original probability compute algorithms, replaced by follow one
            # transition_probability = self.A[self.start_state].get(state, 0)
            # state_observation_likelihood = self.B[state].get(word, default_word_emission)
            # path_probability = transition_probability * state_observation_likelihood

            # using log(probability) as probability to prevent number to be too small
            transition_probability = self.A[self.start_state].get(state, self.very_small_probability)

            state_observation_likelihood = self.B[state].get(word, self.very_small_probability)

            path_probability = transition_probability + state_observation_likelihood

            self.trellis[state][0] = path_probability

            step_state = "{}_{}".format(state, 0)
            self.G.add_node(step_state)

            self.G.add_edge(self.start_state, step_state,
                            probability=path_probability,  traceback=False,
                            state_from=self.start_state, state_to=state, step=1)

            trackback[state] = {}
            trackback[state][0] = self.start_state

            self.G.add_edge(step_state, self.start_state,
                            probability=path_probability, traceback=True,
                            state_from=state, state_to=self.start_state, step=1)

        # recursion step
        for step in range(1, N):
            word = word_list[step]

            for state in all_states:
                # compute all previous path
                candidate_list = []
                for i in all_states:

                    previous_path_probability = self.trellis[i][step - 1]

                    # NOTE: this is original probability compute algorithms, replaced by follow one
                    # transition_probability = self.A[i].get(state, 0)
                    # state_observation_likelihood = self.B[state].get(word, default_word_emission)
                    #
                    # path_probability = previous_path_probability * transition_probability * state_observation_likelihood

                    # using log(probability) as probability to prevent number to be too small
                    transition_probability = self.A[i].get(state, self.very_small_probability)

                    state_observation_likelihood = self.B[state].get(word, self.very_small_probability)

                    path_probability = previous_path_probability + transition_probability + state_observation_likelihood

                    candidate_list.append([i, path_probability])

                    previous_step_state = "{}_{}".format(i, step - 1)
                    step_state = "{}_{}".format(state, step)
                    self.G.add_node(step_state)

                    self.G.add_edge(previous_step_state, step_state,
                                    probability=path_probability, traceback=False,
                                    state_from=i, state_to=state, step=step)

                sorted_candidate_list = sorted(candidate_list, key=lambda x: x[1],
                                               reverse=True)  # NOTE: descending sort by reverse = True

                most_probability_candidate = sorted_candidate_list[0]
                most_probability_state_name = most_probability_candidate[0]
                most_probability_value = most_probability_candidate[1]

                self.trellis[state][step] = most_probability_value

                trackback[state][step] = most_probability_state_name

                previous_step_state = "{}_{}".format(most_probability_state_name, step - 1)
                step_state = "{}_{}".format(state, step)
                self.G.add_edge(step_state, previous_step_state,
                                probability=most_probability_value, traceback=True,
                                state_from=state, state_to=most_probability_state_name, step=step)

        # termination step
        self.G.add_node(self.end_state)

        candidate_list = []
        for i in all_states:
            previous_path_probability = self.trellis[i][T]

            # NOTE: this is original probability compute algorithms, replaced by follow one
            # transition_probability = self.A[i].get(self.end_state, 0)
            #
            # path_probability = previous_path_probability * transition_probability

            # using log(probability) as probability to prevent number to be too small
            transition_probability = self.A[i].get(self.end_state, self.very_small_probability)

            path_probability = previous_path_probability + transition_probability

            candidate_list.append([i, path_probability])

            previous_step_state = "{}_{}".format(i, T)

            self.G.add_edge(previous_step_state, self.end_state,
                            probability=path_probability, traceback=False,
                            state_from=i, state_to=self.end_state, step=N)

        sorted_candidate_list = sorted(candidate_list, key=lambda x: x[1],
                                       reverse=True)  # NOTE: descending sort by reverse = True)

        most_probability_candidate = sorted_candidate_list[0]
        most_probability_state_name = most_probability_candidate[0]
        most_probability_value = most_probability_candidate[1]

        self.trellis[self.end_state] = {}
        self.trellis[self.end_state][T] = most_probability_value

        trackback[self.end_state] = {}
        trackback[self.end_state][T] = most_probability_state_name

        step_state = "{}_{}".format(most_probability_state_name, T)

        self.G.add_edge(self.end_state, step_state,
                        probability=most_probability_value, traceback=True,
                        state_from=self.end_state, state_to=most_probability_state_name, step=N)

        return trackback

    def predict_state(self, word_list):
        traceback = self._do_predict(word_list)

        N = len(word_list)
        T = N - 1

        reverse_state_sequence = []

        reverse_state_sequence.append(self.end_state)

        state = traceback[self.end_state][T]
        reverse_state_sequence.append(state)

        previous_state = state

        reverse_step = reversed(range(len(word_list)))
        for step in reverse_step:
            state = traceback[previous_state][step]
            reverse_state_sequence.append(state)

            previous_state = state

        return list(reversed(reverse_state_sequence))

    def write_graphml(self, graphml_file):
        if isinstance(self.G, MockedGraph):
            raise ValueError("store_graph is False when init Viterbi, so there no graph")

        nx.write_graphml(
            self.G,
            graphml_file,

            # Determine if numeric types should be generalized. For example,
            # if edges have both int and float 'weight' attributes,
            # we infer in GraphML that both are floats.
            infer_numeric_types=True
        )


if __name__ == "__main__":
    A = {'<start>': {'A': 1.0}, 'C': {'<end>': 1.0}, 'A': {'B': 1.0}, 'B': {'C': 1.0}}
    B = {'C': {'人': 0.5, '中国人': 0.5}, 'A': {'你': 0.5, '我': 0.5}, 'B': {'是': 0.5, '打': 0.5}}
    vocabulary = {'人', '中国人', '你', '我', '是', '打'}
    viterbi = Viterbi(A, B, vocabulary)
    viterbi._do_predict(["我", "打", "中国人"])

    state_sequence = viterbi.predict_state(["我", "是", "中国人"])
    viterbi.write_graphml("output.graphml")
    print(state_sequence)
