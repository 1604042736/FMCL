"""
请参考 https://pypi.org/project/m3u8/ 安装m3u8后将包直接复制到该文件夹下
或者直接删除该文件夹(可能会出现运行结果不一致的情况)
"""

import webbrowser


def about():
    return {
        "3rdparty": [
            {
                "name": "m3u8",
                "description": "v6.0.0",
                "operators": (
                    {
                        "action": lambda: webbrowser.open(
                            "https://github.com/globocom/m3u8"
                        ),
                        "name": "GitHub",
                    },
                ),
            }
        ]
    }
