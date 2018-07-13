[中文版本的 README](README.md)
------------------------------

# MicroHMM

A micro python package for HMM (Hidden Markov Model).

## Python version
Only test by using Python3

## Install
### pip
```bash
pip install MicroHMM
```

### source
```bash
pip install git+https://github.com/howl-anderson/MicroHMM.git
```

## Usage
```python
from MicroHMM.hmm import HMMModel

hmm_model = HMMModel()

# train model line by line
# input format: list of (observation, hidden_state) pair
hmm_model.train_one_line([("我", "人称"), ("是", "动词"), ("中国人", "名词")])
hmm_model.train_one_line([("你", "人称"), ("去", "动词"), ("上海", "名词")])

# predict by line
# input format: list of observation
result = hmm_model.predict(["你", "是", "中国人"])
print(result)
```

Output:
```python
[('你', '人称'), ('是', '动词'), ('中国人', '名词')]
```

## Online demo
[![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/howl-anderson/MicroHMM/master?filepath=.notebooks%2Fdemo.ipynb)

## Used by
* [MicroTokenizer: 一个微型中文分词引擎 | A micro tokenizer for Chinese](https://github.com/howl-anderson/MicroTokenizer)

## Reference
[Speech and Language Processing > Hidden Markov Models](https://web.stanford.edu/~jurafsky/slp3/9.pdf)