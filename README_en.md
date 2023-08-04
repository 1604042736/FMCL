# Functional Minecraft Launcher

![Downloads](https://img.shields.io/github/downloads/1604042736/FMCL/total)
![Stars](https://img.shields.io/github/stars/1604042736/FMCL)
![CodeSize](https://img.shields.io/github/languages/code-size/1604042736/FMCL)
![PoweredBy](https://img.shields.io/badge/Powered%20By-YongjianWang-green.svg)

English | [中文](README.md)

## Introduction

FMCL (Functional Minecraft Launcher) is a cross platform MC launcher written in Python based on PyQt5.

## Contribution

You can do things below or more:

- Add more functions
- Fix Bugs
- Translation
- Improve Help

### Preparation

Execute the following command at the root directory

```shell
pip install -r requirements.txt
```

## Dependency

Please refer to `FMCL/Functions/About/About.py` for details

## Command line parameters

|Parameters     | Introduction                                                                          |
|---------------|---------------------------------------------------------------------------------------|
|`--updated`    | The file indicated after the parameter will be deleted, usually used after the update |
|`--notunpack`  | Unable to decompress and translate, usually used during development                   |
