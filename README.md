# FMCL
![](https://img.shields.io/github/languages/code-size/1604042736/FMCL)
## 简介
`FMCL`(`Functional Minecraft Launcher`)是一个MC启动器
## 支持的操作系统
- `Windows`
未来会支持更多的系统
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
- 通过`QML`改变`Launcher`里面的内容
- 对版本进行管理
- (只)支持离线登录
## 项目结构
```
Main.py                     ->主程序
Globals.py                  ->存储一些全局变量
Core                        ->核心代码(与界面无关的代码)
    Download.py             ->与下载有关的操作
    Game.py                 ->与游戏有关的操作
    Launcher.py             ->启动游戏的操作
QtFBN                       ->自己写的窗口框架
    QFBNNotifyManager.py    ->通知管理
    QFBNWidget.py           ->扩展QWidget
    QFBNWindow.py           ->将根据操作系统选择对应类
    QFBNWindowBasic.py      ->承载QFBNWidget的窗口
    QFBNWindowManager.py    ->软件中窗口的管理
    QFBNWindowWindows.py    ->Windows系统的QFBNWindow实现
Ui                          ->界面
    Downloader              ->下载界面
        ...
    DownloadManager         ->下载管理界面
        ...
    Homepage                ->主页
        ...
    Launcher                ->启动界面
        ...
    Setting                 ->设置界面
        ...
    User                    ->用户界面
        ...
    VersionManager          ->版本管理界面
        ...
    MainWindow.py           ->主窗口
    QCustomButton.py        ->自定义按钮
Scripts                     ->脚本(与软件无关)
    ReleaseBuilder.py       ->构建一个Release版本
```