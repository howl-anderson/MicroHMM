[README written in English](README.en-US.md)
------------------------------

# MicroHMM

一个微型的基于 Python 的 HMM (隐马尔可夫模型) 包.

## Python 版本
只在 Python 3 下进行过测试

## 安装
### pip
```bash
pip install MicroHMM
```

### source
```bash
pip install git+https://github.com/howl-anderson/MicroHMM.git
```

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

## Roadmap
* [TODO] 使用预先 `math.log` 的处理方式，加速运行速度
* [TODO] 解决 `math.log` 在偶然情况写下会出现的 `math domain error`

## Used by
* [MicroTokenizer: 一个微型中文分词引擎 | A micro tokenizer for Chinese](https://github.com/howl-anderson/MicroTokenizer)

## Reference
[Speech and Language Processing > Hidden Markov Models](https://web.stanford.edu/~jurafsky/slp3/9.pdf)