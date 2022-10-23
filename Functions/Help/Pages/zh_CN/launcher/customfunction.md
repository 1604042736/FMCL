# ![Author](https://img.shields.io/badge/Author-YongjianWang-green.svg)

你需要将与新功能有关的程序放到`FMCL/Functions/${功能名}`文件夹中

在该文件夹中的`__init__.py`需要定义如下函数

```python
from PyQt5.QtGui import QIcon
from typing import Callable

def getFunctions() -> list[tuple[str,QIcon,Callable]]:
    """获取所有功能

    Returns:
        list[tuple[str,QIcon,Callable]]: 功能信息列表
                    |    |       |- 点击时执行的操作
         功能显示的名称  功能显示的图标
    """
```
