import os
import shutil
import sys
import zipapp
import traceback
import minecraft_launcher_lib as mll
from zipfile import ZipFile

from Pack import main

root = os.path.abspath("..")


class ReleaseBuilder:
    """构建一个Release"""

    def __init__(self, version) -> None:
        self.version = version
        self.release_path = f"{root}/release/{version}"
        if not os.path.exists(self.release_path):
            os.makedirs(self.release_path)

    @staticmethod
    def call_build(func):
        def wrap(*args):
            try:
                print(f"{func.__doc__}...")
                func(*args)
                print(f"{func.__doc__}完成")
            except:
                traceback.print_exc()
                print(f"{func.__doc__}失败")
                exit()

        return wrap

    @call_build
    def pack(self):
        """打包"""
        main()

    @call_build
    def build_pyz(self):
        """生成pyzw文件"""

        def pack_filter(path):
            """过滤函数"""
            path_str = str(path).replace("\\", "/")
            if (
                path_str.endswith(".py")
                and "Scripts" not in path_str
                and "FMCL" not in path_str
            ):
                if os.path.isfile(root + "/" + path_str):
                    print(f'打包"{path_str}"')
                return True
            else:
                return False

        zipapp.create_archive(
            root + "/",
            os.path.join(self.release_path, f"FMCL_{self.version}.pyzw"),
            main="Main:main",
            filter=pack_filter,
        )

    @call_build
    def build_exe(self):
        """生成exe文件"""
        icon_path = os.path.join(root, "Resources", "Icon", "FMCL.ico")
        pyzw_path = os.path.join(self.release_path, f"FMCL_{self.version}.pyzw")
        extract_path = os.path.join(self.release_path, f"FMCL_{self.version}")
        with ZipFile(pyzw_path) as zipfile:
            zipfile.extractall(extract_path)
        os.remove(f"{extract_path}/__main__.py")
        args = [
            f"cd {extract_path}",
            "&",
            "nuitka",
            "--windows-disable-console",
            "--standalone",
            "--mingw64",
            "--show-memory",
            "--show-progress",
            "--enable-plugin=pyqt5",
            f"--windows-icon-from-ico={icon_path}",
            "--output-dir=.",
            "Main.py",
        ]
        print(f"执行 {' '.join(args)}")
        os.system(" ".join(args))

        if not os.path.exists(f"{extract_path}/Main.dist/minecraft_launcher_lib"):
            os.makedirs(f"{extract_path}/Main.dist/minecraft_launcher_lib")
        shutil.copy(
            f"{mll.__path__[0]}/version.txt",
            f"{extract_path}/Main.dist/minecraft_launcher_lib/version.txt",
        )

    def build(self):
        """生成"""
        self.pack()
        self.build_pyz()
        self.build_exe()


if __name__ == "__main__":
    builder = ReleaseBuilder(sys.argv[1])
    builder.build()
