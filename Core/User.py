import json
import os

import minecraft_launcher_lib as mll
from Setting import Setting


class User:
    setting = {}
    if os.path.exists("FMCL/users.json"):
        setting = json.load(open("FMCL/users.json", encoding="utf-8"))

    @staticmethod
    def create_offline(username: str):
        """创建离线登录用户"""
        User.setting[username] = mll.utils.generate_test_options()
        User.setting[username]["username"] = username
        User.sync()

    @staticmethod
    def create_microsoft():
        """创建微软用户"""
        # FIXME

    @staticmethod
    def get_all_users():
        """获取所有用户"""
        return list(User.setting.keys())

    @staticmethod
    def delete_user(username: str):
        """删除用户"""
        User.setting.pop(username)
        User.sync()

    @staticmethod
    def sync():
        json.dump(User.setting,
                  open("FMCL/users.json", mode="w", encoding="utf-8"))

        value = Setting().get("users")
        for i in User.setting:
            if i not in value:
                value.append(i)

    @staticmethod
    def get_cur_user():
        """获取当前用户"""
        value = Setting().get("users")
        if value:
            return User.setting[value[0]]
        else:
            return None
