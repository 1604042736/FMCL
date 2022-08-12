# FMCL

![](https://img.shields.io/github/languages/code-size/1604042736/FMCL)

[English](README.en.md)

## 简介

`FMCL`(`Functional Minecraft Launcher`)是一个MC启动器

## 项目使用

首先安装所需的模块

```
pip install -r requirements.txt
```

然后直接运行`Main.py`即可

## 注意事项

- 非`Windows`用户无需安装`win32gui`和`pywin32`

## 软件功能

- 原版的下载与运行
- `Forge`版本的下载安装与运行
- `Fabric`版本的下载安装与运行
- `Optifine`版本的下载安装与运行
- 对版本进行管理
- (只)支持离线登录
- 支持更新
- 支持Mod的搜索与下载
- 支持更改主题颜色
- 支持多种语言
- 支持浏览新闻

## 命令行参数

- `--updated filename` 会删除`filename`,一般在更新时删除旧的版本
- `--only module` 导入`module`并显示其中的Ui,默认类名和文件名相同,且一个文件只有一个类

## 项目结构

```
Main.py                     ->主程序
Globals.py                  ->存储一些全局变量
Core                        ->核心代码(与界面无关的代码)
    Download.py             ->与下载有关的操作
    Game.py                 ->与游戏有关的操作
    Launcher.py             ->启动游戏的操作
    Mod.py                  ->与Mod有关的操作
    Update.py               ->与更新有关的操作
    News.py                 ->与新闻有关的操作
QtFBN                       ->自己写的窗口框架
    QFBNDialog.py           ->对话框
    QFBNNotifyManager.py    ->通知管理
    QFBNWidget.py           ->扩展QWidget
    QFBNWindow.py           ->将根据操作系统选择对应类
    QFBNWindowBasic.py      ->承载QFBNWidget的窗口
    QFBNWindowManager.py    ->软件中窗口的管理
    QFBNWindowWindows.py    ->Windows系统的QFBNWindow实现
Resources                   ->存放资源
    Image                   ->图片
Scripts                     ->一些脚本
    IconMaker.py            ->制作图标
    ReleaseBuilder.py       ->构建一个发行版本
Translate                   ->翻译
    English.py              ->英语
Ui                          ->界面
    About                   ->关于界面
        ...
    AllHelp                 ->所有帮助
        ...
    Desktop                 ->桌面界面
        ...
    Downloader              ->下载界面
        ...
    DownloadManager         ->下载管理界面
        ...
    Help                    ->帮助界面(包含了"AllHelp")
        ...
    Homepage                ->主页界面
        ...
    News                    ->新闻界面
        ...
    Setting                 ->设置界面
        ...
    User                    ->用户界面
        ...
    VersionManager          ->版本管理界面
        ...
    MainWindow.py           ->主窗口
    QCustomButton.py        ->自定义按钮
```
