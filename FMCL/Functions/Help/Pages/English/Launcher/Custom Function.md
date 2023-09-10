Programs related to new functions need to be placed in the `FMCL/Functions` folder

In this folder `__init__.py` needs to define the following functions

```python
def functionInfo():
    """Function Information"""

def main(*args):
    """Main program"""
```

You also need to add the following functions if you need to customize your settings

```python
def defaultSetting() -> dict:
    """Default Setting"""
    
def defaultSettingAttr() -> dict:
    """Default Setting Attribute"""
```
