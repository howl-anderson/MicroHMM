import collections


class ForwardAlgorithm(object):
    """
    observations of len T, state-graph of len N
    """
    def __init__(self, A, B, pi, vocabulary):
        self.A = A
        self.B = B
        self.pi = pi
        self.vocabulary = vocabulary
        self.all_status = self.A.keys()

    def get_score(self, observation_sequence):
        self._check_if_all_in_vocabulary(observation_sequence)

        # forward[N,T]
        forward_matrix = collections.defaultdict(dict)

        seq_len = len(observation_sequence)

        # initial step
        first_observation = observation_sequence[0]
        for status in self.all_status:
            forward_matrix[status][0] = self.pi.get(status, 0) * self.B[status].get(first_observation, 0)

        # recurse step
        for step in range(1, len(observation_sequence)):
            observation = observation_sequence[step]
            prev_step = step - 1
            for next_status in self.all_status:
                forward_matrix[next_status][step] = 0
                for prev_status in self.all_status:
                    forward_matrix[next_status][step] += forward_matrix[prev_status][prev_step] * self.A[prev_status].get(next_status, 0)
                forward_matrix[next_status][step] *= self.B[next_status].get(observation, 0)

        # terminal step
        forward_probability = sum(forward_matrix[i][seq_len - 1] for i in self.all_status)

        return forward_probability

    def _check_if_all_in_vocabulary(self, seq):
        for i in seq:
            if i not in self.vocabulary:
                raise ValueError("value {} out of vocabulary".format(i))


if __name__ == "__main__":
    A = {'A': {'B': 1.0}, 'B': {'C': 1.0}, 'C': {}}
    pi = {'A': 1.0}
    B = {'C': {'人': 0.5, '中国人': 0.5}, 'A': {'你': 0.5, '我': 0.5}, 'B': {'是': 0.5, '打': 0.5}}
    vocabulary = {'人', '中国人', '你', '我', '是', '打'}
    forward_algorithm = ForwardAlgorithm(A, B, pi, vocabulary)

    score = forward_algorithm.get_score('我 是 中国人'.split())
    print(score)
