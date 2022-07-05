import os
import sys
from typing import TextIO
import zipapp


class ReleaseBuilder(TextIO):
    """构建一个Release"""
    stdout = sys.stdout  # 保存原来的stdout
    indent = 0  # 当前的缩进

    def __init__(self, version) -> None:
        self.version = version
        self.release_path = f"../Release/{version}"
        if not os.path.exists(self.release_path):
            os.makedirs(self.release_path)

    @staticmethod
    def call_build(func):
        def wrap(*args):
            try:
                print(f"{func.__doc__}...")
                ReleaseBuilder.indent += 1
                func(*args)
                ReleaseBuilder.indent -= 1
                print(f"{func.__doc__}完成")
            except BaseException as e:
                ReleaseBuilder.indent -= 1
                print(f"{func.__doc__}失败: {e}")
                exit()
        return wrap

    @call_build
    def build_pyz(self):
        """生成pyzw文件"""
        filter_file = open('../.gitignore').readlines()
        filter_file.extend(
            ['.git', 'README.md', 'requirements.txt', 'LICENSE', '.gitignore', '.vscode', 'Scripts'])

        for i in range(len(filter_file)):  # 去除末尾的/
            filter_file[i] = filter_file[i].strip()
            if filter_file[i][-1] == '/':
                filter_file[i] = filter_file[i][:-1]

        print("确定过滤的文件:")
        ReleaseBuilder.indent += 1
        for i in filter_file:
            print(i)
        ReleaseBuilder.indent -= 1

        def pack_filter(path):
            """过滤函数"""
            path_str = str(path).replace('\\', '/')
            if path_str.endswith('.ui'):
                return False
            for i in filter_file:
                if i in path_str:
                    return False
            if os.path.isfile("../"+path_str):
                print(f'打包"{path_str}"')
            return True

        zipapp.create_archive('../',
                              os.path.join(
                                  self.release_path, f'FMCL_{self.version}.pyzw'),
                              main='Main:main',
                              filter=pack_filter)

    def build(self):
        """生成"""
        self.build_pyz()

    def write(self, text):
        self.stdout.write(f"{' '*4*self.indent}{text}")


if __name__ == "__main__":
    builder = ReleaseBuilder(sys.argv[1])
    sys.stdout = builder
    builder.build()
