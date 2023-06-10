from Setting import Setting

from .Explorer import Explorer


def defaultSetting() -> dict:
    return {
        "explorer.desktop.background_image": "",
        "explorer.desktop.item_clicked_actions": ["Launcher", "GameManager"]
    }


def defaultSettingAttr() -> dict:
    return {
        "explorer": {
            "name": "Explorer"
        },
        "explorer.desktop": {
            "name": "桌面"
        },
        "explorer.desktop.background_image": {
            "name": "背景图片"
        },
        "explorer.desktop.item_clicked_actions": {
            "name": "游戏右键操作"
        }
    }


def main():
    explorer = Explorer()
    explorer.show()
