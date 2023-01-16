def getColors() -> dict:
    from .Setting import Setting
    color = Setting().get("system.theme_color")
    color_num = int(color.replace("#", ""), base=16)

    opp_color_num = color_num ^ (2**(len(bin(color_num))-2)-1)  # 相反的颜色
    opp_color = "#"+hex(opp_color_num).replace("0x", "").rjust(6, "0")

    dark_color = color.replace("#", "")
    dark_color = dark_color[:2], dark_color[2:4], dark_color[4:]
    dark_color = list(map(lambda x: int(x, base=16), dark_color))
    for i in range(len(dark_color)):
        if dark_color[i]-55 >= 0:
            dark_color[i] -= 55
        dark_color[i] = hex(dark_color[i]).replace("0x", "").rjust(2, "0")
    dark_color = ''.join(map(str, dark_color))
    dark_color = "#"+dark_color

    return {
        "color": color,
        "opp_color": opp_color,
        "dark_color": dark_color
    }


W_D_TITLEBUTTON = 46  # 标题栏按钮的默认宽度
H_D_TITLEBUTTON = 32  # 标题栏按钮的默认高度


def S_D_TITLEBUTTON():
    """标题栏按钮的默认样式"""
    colors = getColors()
    return f"""
QPushButton{{
    border:none;
}}
QPushButton:hover{{
    background-color:{colors['dark_color']};
}}
"""


def S_D_TITLE():
    """标题栏默认样式"""
    colors = getColors()
    return f"""
QWidget#titleBar{{
    background-color:{colors['color']};
}}
"""


W_D_TASKBUTTON = 100  # 任务栏按钮的默认高度


def S_D_TASKBUTTON():
    """任务栏按钮的默认样式"""
    colors = getColors()
    return f"""
QPushButton{{
    border:none;
}}
QPushButton:hover{{
    background-color:{colors['dark_color']};
}}
"""


def S_S_TASKBUTTON():
    """任务栏按钮的选中时的样式"""
    colors = getColors()
    return f"""
QPushButton{{
    border: none;
    background-color:{colors['dark_color']}; 
}}
"""


W_PANEL = 46  # 面板宽度
W_PANEL_EXPAND = W_PANEL*3  # 面板展开时的宽度
H_PANELBUTTON = 46  # 面板按钮高度


def S_D_PANELBUTTON():
    """面板按钮默认样式"""
    colors = getColors()
    return f"""
QPushButton{{
    border: none;
    text-align: left;
}}
QPushButton:hover{{
    background-color: {colors['dark_color']};
}}
QPushButton:checked{{
    border-left: 2px solid black;
}}
"""


def S_D_PANEL():
    """面板默认样式"""
    colors = getColors()
    return f"""
QFrame{{
    background-color: {colors['color']};
    border-right: 1px solid rgb(245, 245, 245);
}}
"""


# explorer的宽高
W_EXPLORER = 1000
H_EXPLORER = 618

# 设置的宽高
W_SETTING = W_EXPLORER
H_SETTING = H_EXPLORER
