# ![Author](https://img.shields.io/badge/Author-YongjianWang-green.svg)

你需要创建`FMCL/Help/__init__.py`并在里面定义如下函数

```python
def getIndexes(language:str) -> dict[str,str]:
    """获取帮助文件索引

    Args:
        language (str): 当前软件的语言

    Returns:
        dict[str,str]: 帮助文件索引
              |   |- 索引对应的帮助文件
          索引，多级索引间用'.'分割
    """
```

帮助文件必须是Markdown格式的
