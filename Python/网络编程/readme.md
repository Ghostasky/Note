# 第一章

先来个argparse模块

首先

```python
import argparse
parse = argparse.ArgumentParser()
parse.parse_args()
```

## 位置参数

```python
import argparse

parse = argparse.ArgumentParser()
parse.add_argument("qwe")
args = parse.parse_args()
print(args.qwe)
```

 `add_argument()` 方法，该方法用于指定程序能够接受哪些命令行选项。

稍微改的有用点：

```python
parse.add_argument("qwe", help="qwe can echo string you input")
```

```shell
usage: aa.py [-h] qwe

positional arguments:
  qwe         qwe can echo string you input

optional arguments:
  -h, --help  show this help message and exit
```

还可以：

```python
parse.add_argument("qwe", help="qwe can echo string you input", type=int)
args = parse.parse_args()
print(args.qwe ** 2)
```

输出为参数的平方

## 可选参数

```python
parse.add_argument("--verbosity", help="increase output verbosity")
args = parse.parse_args()
if args.verbosity:
    print("verbosity turn on")
```

这样写--verbosity参数时后面必须跟一个参数，如果不想跟的话可以加一个`action = "store_true"`

### 短选项

`parse.add_argument( "-v", "--verbosity", help="increase output verbosity", action="store_true")`

