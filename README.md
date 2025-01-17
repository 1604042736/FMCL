# Functional Minecraft Launcher

![Downloads](https://img.shields.io/github/downloads/wyj2006/FMCL/total)
![Stars](https://img.shields.io/github/stars/wyj2006/FMCL)
![CodeSize](https://img.shields.io/github/languages/code-size/wyj2006/FMCL)
![PoweredBy](https://img.shields.io/badge/Powered%20By-YongjianWang-green.svg)

[English](README_en.md) | 中文

## 介绍

FMCL (Functional Minecraft Launcher) 是一个用Python编写的基于PyQt5的跨平台的MC启动器

## 贡献

您可以做一下几件事或者更多:

- 添加更多功能
- 修复Bug
- 翻译
- 完善帮助

### 准备

在根目录执行以下命令

```shell
pip install -r requirements.txt
```

以下是非必要的命令

```shell
mkdir Pack
cd Scripts
python Pack.py
```

## 依赖

详见`Kernel.py`中的`Kernel.getAbout`函数

## 命令行参数

| 参数          | 简介                                    |
|---------------|----------------------------------------|
|`--updated`    |将会删除参数后面指示的文件,一般在更新后使用 |
