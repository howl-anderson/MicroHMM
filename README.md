[README written in English](README.en-US.md)
------------------------------

# MicroHMM

一个微型的基于Python 的 HMM (隐马尔可夫模型) 包.

## Python 版本
为了使用 `math.inf`，这个软件包要求 python >= 3.5

## 使用
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

输出：
```python
[('你', 'A'), ('去', 'B'), ('上海', 'C')]
```

## 在线演示
**TODO**

## Reference
[Speech and Language Processing > Hidden Markov Models](https://web.stanford.edu/~jurafsky/slp3/9.pdf)