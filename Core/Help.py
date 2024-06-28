import logging
import os
import traceback

from importlib import import_module

from Core.Function import Function


class Help:
    """帮助"""

    PATH = ["FMCL/Help", "FMCL/Default/FMCL/Help"]

    @staticmethod
    def get_index():
        def merge(a: dict, b: dict):
            for key, val in b.items():
                if key not in a:
                    a[key] = val
                elif isinstance(val, dict) and isinstance(a[key], dict):
                    merge(a[key], val)
                elif isinstance(val, list) and isinstance(a[key], list):
                    a[key].extend(val)
                else:
                    a[key] = val

        helpindex = {}
        for root in Help.PATH:
            if not os.path.exists(root):
                continue
            for i in os.listdir(root):
                try:
                    module = import_module(f"FMCL.Help.{i}")
                    merge(helpindex, getattr(module, "helpIndex", lambda: {})())
                except:
                    logging.error(traceback.format_exc())
        for i in Function.get_all_help_index():
            merge(helpindex, i)
        return helpindex

    @staticmethod
    def get_index_attr(helpindex: dict, id: str):
        """通过id获得帮助索引中的属性"""
        splitid = id.split(".")
        val = helpindex
        for i in splitid:
            val = val[i]
        return val
