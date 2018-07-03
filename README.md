# MicroHMM

A micro python package for HMM (Hidden Markov Model).

## Python version
python 3.5+

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

## Online demo
**TODO**