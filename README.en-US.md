[中文版本的 README](README.md)
------------------------------

# MicroHMM

A micro python package for HMM (Hidden Markov Model).

## Python version
python >= 3.5 for using `math.inf`

## Usage
```python
from MicroHMM.hmm import HMMModel

hmm_model = HMMModel()

# train model line by line
# input format: list of (observation, hidden_state) pair
hmm_model.train_one_line([("我", "A"), ("是", "B"), ("中国人", "C")])
hmm_model.train_one_line([("你", "A"), ("去", "B"), ("上海", "C")])

# predict by line
# input format: list of observation
result = hmm_model.predict(["你", "去", "上海"])
print(result)
```

Output:
```python
[('你', 'A'), ('去', 'B'), ('上海', 'C')]
```

## Online demo
**TODO**

## Reference
[Speech and Language Processing > Hidden Markov Models](https://web.stanford.edu/~jurafsky/slp3/9.pdf)