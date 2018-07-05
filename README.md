[README written in English](README.en-US.md)
------------------------------

# MicroHMM

一个微型的基于Python 的 HMM (隐马尔可夫模型) 包.

## Python 版本
只在 Python 3 下进行过测试

## 使用
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

输出：
```python
[('你', '人称'), ('是', '动词'), ('中国人', '名词')]
```

## 在线演示
[![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/howl-anderson/MicroHMM/master?filepath=.notebooks%2Fdemo.ipynb)

## Reference
[Speech and Language Processing > Hidden Markov Models](https://web.stanford.edu/~jurafsky/slp3/9.pdf)