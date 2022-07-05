"""
QtFBN,Qt Frameless but Native
有以下几种目的:
1.自定义标题栏
2.保留原生窗口特性
3.方便的管理软件中的窗口
"""
import Globals as g
from PyQt5.QtWidgets import QPushButton
import qtawesome as qta

manager = None  # 一个软件至多有一个QFBNWindowManager

# 以下下内容非必要(on_any_win_ready必要)


def on_any_win_ready(win) -> None:
    if win is not manager and manager!=None:
        win.pb_home = QPushButton(win.win.title)
        win.pb_home.resize(win.win.title_button_width,
                           win.win.title_height)
        win.pb_home.setObjectName('pb_home')
        win.pb_home.setIcon(qta.icon('msc.window'))
        win.pb_home.clicked.connect(manager.activateWindow)
        win.win.add_right_widget(win.pb_home)

    win.pb_dmgr = QPushButton(win.win.title)
    win.pb_dmgr.resize(win.win.title_button_width,
                       win.win.title_height)
    win.pb_dmgr.setObjectName('pb_dmgr')
    win.pb_dmgr.setIcon(qta.icon('ri.download-2-fill'))
    win.pb_dmgr.clicked.connect(lambda: g.dmgr.show())
    win.pb_dmgr.hide()
    win.win.add_right_widget(win.pb_dmgr)
    if g.dmgr.task_num: #只有在有任务的时侯才会显示
        win.pb_dmgr.show()

    g.dmgr.NoTask.connect(lambda: notask(win))
    g.dmgr.HasTask.connect(lambda: hastask(win))


def notask(win):
    win.pb_dmgr.hide()
    win.win.resize_title_widgets()


def hastask(win):
    win.pb_dmgr.show()
    win.win.resize_title_widgets()
