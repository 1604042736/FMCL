from PyQt5.QtCore import QObject, QEvent

W_D_TITLEBUTTON = 46  # 标题栏按钮的默认宽度
H_D_TITLEBUTTON = 32  # 标题栏按钮的默认高度

# 标题栏按钮的默认样式
S_D_TITLEBUTTON = """
QPushButton{
    border:none;
}
QPushButton:hover{
    background-color:rgb(200,200,200);
}
"""

W_D_TASKBUTTON = 100  # 任务栏按钮的默认高度
# 任务栏按钮的默认样式
S_D_TASKBUTTON = """
QPushButton{
    border:none;
}
QPushButton:hover{
    background-color:rgb(200,200,200);
}
"""
# 任务栏按钮的选中时的样式
S_S_TASKBUTTON = """
QPushButton{
    border:none;
    background-color:rgb(200,200,200);
}
"""

W_PANEL = 46  # 面板宽度
W_PANEL_EXPAND = W_PANEL*3  # 面板展开时的宽度
H_PANELBUTTON = 46  # 面板按钮高度
# 面板按钮默认样式
S_D_PANELBUTTON = """
QPushButton{
    border:none;
    text-align:left;
}
QPushButton:hover{
    background-color:rgb(200,200,200);
}
QPushButton:checked{
    border-left:2px solid black;
}
"""
# 面板默认样式
S_D_PANEL = """
QFrame{
    background-color:rgb(255,255,255);
    border-right:1px solid rgb(245,245,245);
}
"""

# explorer的宽高
W_EXPLORER = 1000
H_EXPLORER = 618

# 设置的宽高
W_SETTING = W_EXPLORER
H_SETTING = H_EXPLORER
