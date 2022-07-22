# FMCL
![](https://img.shields.io/github/languages/code-size/1604042736/FMCL)
## Introduction
`FMCL`(`Functional Minecraft Launcher`) is a Minecraft Launcher
## Support Systems
- `Windows`

We will support more systems in the future
## Project Usage
First install required modules
```
pip install -r requirements.txt
```
Then run `Main.py` directly
## Note
- Non `Windows`users do not need to install`win32gui`和`pywin32`
## APP Functions
- Download and run Minecraft
- Download,install and run Minecraft with `Forge`
- Download,install and run Minecraft with `Fabric`
- Download,install and run Minecraft with `Optifine`
- Change content in `Launcher` through `QML`
- Manage versions
- (Only)Support offline login 
- Support updata
- Support Mods' search and download
- Support change theme color
## Project Structure
```
Main.py                     ->Main program
Globals.py                  ->Store globals variables
Core                        ->Core code(Has nothing to do with UI code)
    Download.py             ->Download related operations
    Game.py                 ->Game related operations
    Launcher.py             ->Launching game related operations
    Mod.py                  ->Mod related operations
    Updata.py               ->Updata related operations
QtFBN                       ->Window framework written by myself
    QFBNNotifyManager.py    ->Notify Manager
    QFBNWidget.py           ->Extend QWidget
    QFBNWindow.py           ->Selected class according to the operating system
    QFBNWindowBasic.py      ->Window hosting QFBNWidget
    QFBNWindowManager.py    ->Manage windows in APP
    QFBNWindowWindows.py    ->QFBNWindow in Windows system
Ui                          ->UI
    Desktop                 ->Desktop Ui
        ...
    Downloader              ->Download UI
        ...
    DownloadManager         ->Download Manager UI
        ...
    Homepage                ->Homepage
        ...
    Setting                 ->Setting UI
        ...
    User                    ->User UI
        ...
    VersionManager          ->Version Manager UI
        ...
    MainWindow.py           ->Main Window
    QCustomButton.py        ->Custom button
```