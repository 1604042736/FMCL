# Functional Minecraft Launcher

![Downloads](https://img.shields.io/github/downloads/wyj2006/FMCL/total)
![Stars](https://img.shields.io/github/stars/wyj2006/FMCL)
![CodeSize](https://img.shields.io/github/languages/code-size/wyj2006/FMCL)
![PoweredBy](https://img.shields.io/badge/Powered%20By-YongjianWang-green.svg)

English | [中文](README.md)

## Introduction

FMCL (Functional Minecraft Launcher) is a cross platform MC launcher written in Python based on PyQt5.

## Contribution

You can do things below or more:

- Add more functions
- Fix Bugs
- Translate
- Improve Help

### Preparation

Execute the following command at the root directory

```shell
pip install -r requirements.txt
```

The following are non-essential commands

```shell
mkdir Pack
cd Scripts
python Pack.py
```

## Dependency

For details, see the `Kernel.getAbout` function in `Kernel.py`

## Command line parameters

|Parameters     | Introduction                                                                          |
|---------------|---------------------------------------------------------------------------------------|
|`--updated`    | The file indicated after the parameter will be deleted, usually used after the update |
