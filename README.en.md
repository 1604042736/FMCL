# FMCL

![](https://img.shields.io/github/languages/code-size/1604042736/FMCL)

## Introduction

`FMCL`(`Functional Minecraft Launcher`) is a Minecraft Launcher

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
- Manage versions
- (Only)Support offline login
- Support update
- Support Mods' search and download
- Support change theme color
- Support more languages
- Support view news
- Support version isolate and specific setting

## Command line parameters

- `--updated filename` will delete `filename`. Generally, the old version will be deleted when updating

- `--only module` import `module` and display UI in it. The default class name is the same as the file name, and there is only one class in a file

## Project Structure

```
Main.py                     ->Main program
Globals.py                  ->Store globals variables
Core                        ->Core code(Has nothing to do with UI code)
    Download.py             ->Download related operations
    Game.py                 ->Game related operations
    Launcher.py             ->Launching game related operations
    Mod.py                  ->Mod related operations
    Update.py               ->Update related operations
    News.py                 ->News related operations
QtFBN                       ->Window framework written by myself
    QFBNDialog.py           ->Dialog
    QFBNNotifyManager.py    ->Notify Manager
    QFBNWidget.py           ->Extend QWidget
    QFBNWindow.py           ->Selected class according to the operating system
    QFBNWindowBasic.py      ->Window hosting QFBNWidget
    QFBNWindowManager.py    ->Manage windows in APP
    QFBNWindowWindows.py    ->QFBNWindow in Windows system
Resources                   ->Save resources
    Image                   ->Images
Scripts                     ->Some scripts
    IconMaker.py            ->Make icon
    ReleaseBuilder.py       ->Build a release version
Translate                   ->Translate
    Chinese.py              ->Chinese
    English.py              ->English
Ui                          ->UI
    About                   ->About UI
        ...
    AllHelp                 ->All help
        ...
    Desktop                 ->Desktop Ui
        ...
    Downloader              ->Download UI
        ...
    DownloadManager         ->Download Manager UI
        ...
    Help                    ->Help UI(Content "AllHelp")
        ...
    Homepage                ->Homepage UI
        ...
    News                    ->News UI
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
