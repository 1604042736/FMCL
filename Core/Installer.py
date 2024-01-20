"""对minecraft_launcher_lib的部分函数进行改写, 以使用多线程"""
import logging
import random
import subprocess
import tempfile
import requests
import shutil
import json
import os
import zipfile

from minecraft_launcher_lib._helper import (
    download_file,
    parse_rule_list,
    inherit_json,
    empty,
    get_user_agent,
    check_path_inside_minecraft_directory,
    extract_file_from_zip,
)
from minecraft_launcher_lib._internal_types.shared_types import (
    ClientJson,
    ClientJsonLibrary,
)
from minecraft_launcher_lib.natives import extract_natives_file, get_natives
from minecraft_launcher_lib._internal_types.install_types import AssetsJson
from typing import List, Optional, Union
from minecraft_launcher_lib.exceptions import (
    VersionNotFound,
    UnsupportedVersion,
    ExternalProgramError,
)
from minecraft_launcher_lib.types import CallbackDict
from minecraft_launcher_lib._internal_types.forge_types import ForgeInstallProfile
from minecraft_launcher_lib.utils import is_version_valid
from minecraft_launcher_lib.fabric import (
    is_minecraft_version_supported,
    get_latest_loader_version,
    get_latest_installer_version,
)
from minecraft_launcher_lib.forge import forge_processors

from PyQt5.QtCore import QCoreApplication

from Setting import Setting

from Core.Task import Task

_translate = QCoreApplication.translate

MAX_POOL_SIZE = 5


class Installer:
    def install_libraries(
        self,
        id: str,
        libraries: List[ClientJsonLibrary],
        path: str,
        callback: CallbackDict,
    ) -> Task:
        """
        Install all libraries
        """
        task = Task(
            _translate("Installer", "下载库"),
            callback.get("getCurTask", lambda _: None)(),
        )

        session = requests.session()

        def get(callback):
            callback.get("setMax", empty)(len(libraries))
            tasks = []
            for count, i in enumerate(libraries):

                def work(count, i, callback):
                    # Check, if the rules allow this lib for the current system
                    if "rules" in i and not parse_rule_list(i["rules"], {}):
                        return

                    # Turn the name into a path
                    current_path = os.path.join(path, "libraries")
                    if "url" in i:
                        if i["url"].endswith("/"):
                            download_url = i["url"][:-1]
                        else:
                            download_url = i["url"]
                    else:
                        download_url = "https://libraries.minecraft.net"

                    try:
                        lib_path, name, version = i["name"].split(":")[0:3]
                    except ValueError:
                        return

                    for lib_part in lib_path.split("."):
                        current_path = os.path.join(current_path, lib_part)
                        download_url = f"{download_url}/{lib_part}"

                    try:
                        version, fileend = version.split("@")
                    except ValueError:
                        fileend = "jar"

                    jar_filename = f"{name}-{version}.{fileend}"
                    download_url = f"{download_url}/{name}/{version}"
                    current_path = os.path.join(current_path, name, version)
                    native = get_natives(i)

                    # Check if there is a native file
                    if native != "":
                        jar_filename_native = f"{name}-{version}-{native}.jar"
                    jar_filename = f"{name}-{version}.{fileend}"
                    download_url = f"{download_url}/{jar_filename}"

                    # Try to download the lib
                    try:
                        download_file(
                            download_url,
                            os.path.join(current_path, jar_filename),
                            callback=callback,
                            session=session,
                            minecraft_directory=path,
                        )
                    except Exception:
                        pass

                    if "downloads" not in i:
                        if "extract" in i:
                            extract_natives_file(
                                os.path.join(current_path, jar_filename_native),
                                os.path.join(path, "versions", id, "natives"),
                                i["extract"],
                            )
                        return

                    if (
                        "artifact" in i["downloads"]
                        and i["downloads"]["artifact"]["url"] != ""
                        and "path" in i["downloads"]["artifact"]
                    ):
                        download_file(
                            i["downloads"]["artifact"]["url"],
                            os.path.join(
                                path, "libraries", i["downloads"]["artifact"]["path"]
                            ),
                            callback,
                            sha1=i["downloads"]["artifact"]["sha1"],
                            session=session,
                            minecraft_directory=path,
                        )
                    if native != "":
                        download_file(i["downloads"]["classifiers"][native]["url"], os.path.join(current_path, jar_filename_native), callback, sha1=i["downloads"]["classifiers"][native]["sha1"], session=session, minecraft_directory=path)  # type: ignore
                        if "extract" in i:
                            extract_natives_file(
                                os.path.join(current_path, jar_filename_native),
                                os.path.join(path, "versions", id, "natives"),
                                i["extract"],
                            )

                task_work = Task(
                    f'{_translate("Installer","处理")}{i["name"]}',
                    task,
                    lambda callback, c=count, i=i: work(c, i, callback),
                )
                if count - MAX_POOL_SIZE >= 0:
                    task_work.waittasks.append(tasks[count - MAX_POOL_SIZE])
                tasks.append(task_work)
                task_work.start()
                callback.get("setProgress", empty)(count + 1)

        task_get = Task(_translate("Installer", "获取库"), task, get)
        return task

    def install_assets(
        self, data: ClientJson, path: str, callback: CallbackDict
    ) -> Task:
        """
        Install all assets
        """
        task = Task(
            _translate("Installer", "下载资源"),
            callback.get("getCurTask", lambda _: None)(),
        )
        # Old versions don't have this
        if "assetIndex" not in data:
            return task

        session = requests.session()

        assets_data: AssetsJson = {}

        def prepare(callback):
            nonlocal assets_data

            download_file(
                data["assetIndex"]["url"],
                os.path.join(path, "assets", "indexes", data["assets"] + ".json"),
                callback,
                sha1=data["assetIndex"]["sha1"],
                session=session,
            )
            with open(
                os.path.join(path, "assets", "indexes", data["assets"] + ".json")
            ) as f:
                assets_data = json.load(f)

        task_prepare = Task(
            _translate("Installer", "准备工作"),
            task,
            prepare,
        )

        def work(callback):
            callback.get("setMax", empty)(len(assets_data["objects"].values()))
            tasks = []
            for i, value in enumerate(assets_data["objects"].values()):
                task_download = Task(
                    f'{_translate("Installer","下载")}{value["hash"]}',
                    task,
                    lambda callback, value=value: download_file(
                        "https://resources.download.minecraft.net/"
                        + value["hash"][:2]
                        + "/"
                        + value["hash"],
                        os.path.join(
                            path,
                            "assets",
                            "objects",
                            value["hash"][:2],
                            value["hash"],
                        ),
                        callback,
                        sha1=value["hash"],
                        session=session,
                        minecraft_directory=path,
                    ),
                )
                if i - MAX_POOL_SIZE >= 0:
                    task_download.waittasks.append(tasks[i - MAX_POOL_SIZE])
                tasks.append(task_download)
                task_download.start()
                callback.get("setProgress", empty)(i + 1)

        task_work = Task(_translate("Installer", "获取资源"), task, work, [task_prepare])
        return task

    def do_version_install(
        self,
        versionid: str,
        path: str,
        callback: CallbackDict,
        url: Optional[str] = None,
        sha1: Optional[str] = None,
    ) -> None:
        """
        Installs the given version
        """
        # Download and read versions.json
        if url:
            download_file(
                url,
                os.path.join(path, "versions", versionid, versionid + ".json"),
                callback,
                sha1=sha1,
                minecraft_directory=path,
            )

        with open(
            os.path.join(path, "versions", versionid, versionid + ".json"),
            "r",
            encoding="utf-8",
        ) as f:
            versiondata: ClientJson = json.load(f)

        # For Forge
        if "inheritsFrom" in versiondata:
            try:
                self.install_minecraft_version(
                    versiondata["inheritsFrom"], path, callback=callback
                )
            except VersionNotFound:
                pass
            versiondata = inherit_json(versiondata, path)

        task_install_libraries = self.install_libraries(
            versiondata["id"], versiondata["libraries"], path, callback
        )
        task_install_assets = self.install_assets(versiondata, path, callback)
        task_install_libraries.start()
        task_install_assets.start()
        Task.waitTasks(
            (
                task_install_libraries,
                task_install_assets,
            ),
            callback,
        )

        # Download logging config
        if "logging" in versiondata:
            if len(versiondata["logging"]) != 0:
                logger_file = os.path.join(
                    path,
                    "assets",
                    "log_configs",
                    versiondata["logging"]["client"]["file"]["id"],
                )
                download_file(
                    versiondata["logging"]["client"]["file"]["url"],
                    logger_file,
                    callback,
                    sha1=versiondata["logging"]["client"]["file"]["sha1"],
                    minecraft_directory=path,
                )

        # Download minecraft.jar
        if "downloads" in versiondata:
            download_file(
                versiondata["downloads"]["client"]["url"],
                os.path.join(
                    path, "versions", versiondata["id"], versiondata["id"] + ".jar"
                ),
                callback,
                sha1=versiondata["downloads"]["client"]["sha1"],
                minecraft_directory=path,
            )

        # Need to copy jar for old forge versions
        if (
            not os.path.isfile(
                os.path.join(
                    path, "versions", versiondata["id"], versiondata["id"] + ".jar"
                )
            )
            and "inheritsFrom" in versiondata
        ):
            inherits_from = versiondata["inheritsFrom"]
            inherit_path = os.path.join(
                path, "versions", inherits_from, f"{inherits_from}.jar"
            )
            check_path_inside_minecraft_directory(path, inherit_path)
            shutil.copyfile(
                os.path.join(
                    path, "versions", versiondata["id"], versiondata["id"] + ".jar"
                ),
                inherit_path,
            )

    def install_minecraft_version(
        self,
        versionid: str,
        minecraft_directory: Union[str, os.PathLike],
        callback: Optional[CallbackDict] = None,
    ) -> None:
        if isinstance(minecraft_directory, os.PathLike):
            minecraft_directory = str(minecraft_directory)
        if callback is None:
            callback = {}
        if os.path.isfile(
            os.path.join(
                minecraft_directory, "versions", versionid, f"{versionid}.json"
            )
        ):
            self.do_version_install(versionid, minecraft_directory, callback)
            return
        version_list = requests.get(
            "https://launchermeta.mojang.com/mc/game/version_manifest_v2.json",
            headers={"user-agent": get_user_agent()},
        ).json()
        for i in version_list["versions"]:
            if i["id"] == versionid:
                self.do_version_install(
                    versionid,
                    minecraft_directory,
                    callback,
                    url=i["url"],
                    sha1=i["sha1"],
                )
                return
        raise VersionNotFound(versionid)

    def install_forge_version(
        self,
        versionid: str,
        path: Union[str, os.PathLike],
        callback: Optional[CallbackDict] = None,
        java: Optional[Union[str, os.PathLike]] = None,
    ) -> None:
        if callback is None:
            callback = {}

        FORGE_DOWNLOAD_URL = "https://files.minecraftforge.net/maven/net/minecraftforge/forge/{version}/forge-{version}-installer.jar"
        temp_file_path = os.path.join(
            Setting()["system.temp_dir"],
            "forge-installer-" + str(random.randrange(1, 100000)) + ".tmp",
        )

        if not download_file(
            FORGE_DOWNLOAD_URL.format(version=versionid), temp_file_path, callback
        ):
            raise VersionNotFound(versionid)

        zf = zipfile.ZipFile(temp_file_path, "r")

        # Read the install_profile.json
        with zf.open("install_profile.json", "r") as f:
            version_content = f.read()

        version_data: ForgeInstallProfile = json.loads(version_content)
        forge_version_id = (
            version_data["version"]
            if "version" in version_data
            else version_data["install"]["version"]
        )
        minecraft_version = (
            version_data["minecraft"]
            if "minecraft" in version_data
            else version_data["install"]["minecraft"]
        )

        # Make sure, the base version is installed
        callback.get("setStatus", empty)("")
        task_install_mc = Task(
            f'{_translate("Installer","安装")}{minecraft_version}',
            callback.get("getCurTask", lambda _: None)(),
            lambda callback: self.install_minecraft_version(
                minecraft_version, path, callback=callback
            ),
        )
        task_install_mc.start()
        Task.waitTasks((task_install_mc,), callback)

        # Install all needed libs from install_profile.json
        if "libraries" in version_data:
            task_install_libraries = self.install_libraries(
                minecraft_version, version_data["libraries"], str(path), callback
            )
            task_install_libraries.start()
            Task.waitTasks((task_install_libraries,), callback)

        # Extract the version.json
        version_json_path = os.path.join(
            path, "versions", forge_version_id, forge_version_id + ".json"
        )
        try:
            extract_file_from_zip(
                zf, "version.json", version_json_path, minecraft_directory=path
            )
        except KeyError:
            if "versionInfo" in version_data:
                with open(version_json_path, "w", encoding="utf-8") as f:
                    json.dump(
                        version_data["versionInfo"], f, ensure_ascii=False, indent=4
                    )

        # Extract forge libs from the installer
        forge_lib_path = os.path.join(
            path, "libraries", "net", "minecraftforge", "forge", versionid
        )
        try:
            extract_file_from_zip(
                zf,
                "maven/net/minecraftforge/forge/{version}/forge-{version}-universal.jar".format(
                    version=versionid
                ),
                os.path.join(forge_lib_path, "forge-" + versionid + "-universal.jar"),
                minecraft_directory=path,
            )
        except KeyError:
            pass

        try:
            extract_file_from_zip(
                zf,
                "forge-{version}-universal.jar".format(version=versionid),
                os.path.join(forge_lib_path, f"forge-{versionid}.jar"),
                minecraft_directory=path,
            )
        except KeyError:
            pass

        try:
            extract_file_from_zip(
                zf,
                f"maven/net/minecraftforge/forge/{versionid}/forge-{versionid}.jar",
                os.path.join(forge_lib_path, f"forge-{versionid}.jar"),
                minecraft_directory=path,
            )
        except KeyError:
            pass

        # Extract the client.lzma
        lzma_path = os.path.join(
            Setting()["system.temp_dir"],
            "lzma-" + str(random.randrange(1, 100000)) + ".tmp",
        )
        try:
            extract_file_from_zip(zf, "data/client.lzma", lzma_path)
        except KeyError:
            pass

        zf.close()

        # Install the rest with the vanilla function
        callback.get("setStatus", empty)("")
        task_install_mc = Task(
            f'{_translate("Installer","安装")}{forge_version_id}',
            callback.get("getCurTask", lambda _: None)(),
            lambda callback: self.install_minecraft_version(
                forge_version_id, str(path), callback=callback
            ),
        )
        task_install_mc.start()
        Task.waitTasks((task_install_mc,), callback)

        # Run the processors
        if "processors" in version_data:
            forge_processors(
                version_data,
                str(path),
                lzma_path,
                temp_file_path,
                callback,
                "java" if java is None else str(java),
            )

        # Delete the temporary files
        os.remove(temp_file_path)
        if os.path.isfile(lzma_path):
            os.remove(lzma_path)

    def install_fabric(
        self,
        minecraft_version: str,
        minecraft_directory: Union[str, os.PathLike],
        loader_version: Optional[str] = None,
        callback: Optional[CallbackDict] = None,
        java: Optional[Union[str, os.PathLike]] = None,
    ) -> None:
        path = str(minecraft_directory)
        if not callback:
            callback = {}

        # Check if the given version exists
        if not is_version_valid(minecraft_version, minecraft_directory):
            raise VersionNotFound(minecraft_version)

        # Check if the given Minecraft version supported
        if not is_minecraft_version_supported(minecraft_version):
            raise UnsupportedVersion(minecraft_version)

        # Get latest loader version if not given
        if not loader_version:
            loader_version = get_latest_loader_version()

        # Make sure the Minecraft version is installed
        task_install_mc = Task(
            f'{_translate("Installer","安装")}{minecraft_version}',
            callback.get("getCurTask", lambda _: None)(),
            lambda callback: self.install_minecraft_version(
                minecraft_version, path, callback=callback
            ),
        )
        task_install_mc.start()
        Task.waitTasks((task_install_mc,), callback)

        # Get installer version
        installer_version = get_latest_installer_version()
        installer_download_url = f"https://maven.fabricmc.net/net/fabricmc/fabric-installer/{installer_version}/fabric-installer-{installer_version}.jar"

        # Generate a temporary path for downloading the installer
        installer_path = os.path.join(
            Setting()["system.temp_dir"],
            f"fabric-installer-{random.randrange(100, 10000)}.tmp",
        )

        # Download the installer
        download_file(installer_download_url, installer_path, callback=callback)

        # Run the installer see https://fabricmc.net/wiki/install#cli_installation
        callback.get("setStatus", empty)("Running fabric installer")
        command = [
            "java" if java is None else str(java),
            "-jar",
            installer_path,
            "client",
            "-dir",
            path,
            "-mcversion",
            minecraft_version,
            "-loader",
            loader_version,
            "-noprofile",
            "-snapshot",
        ]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            raise ExternalProgramError(command, result.stdout, result.stderr)

        # Delete the installer we don't need them anymore
        os.remove(installer_path)

        # Install all libs of fabric
        fabric_minecraft_version = f"fabric-loader-{loader_version}-{minecraft_version}"

        task_install_mc = Task(
            f'{_translate("Installer","安装")}{fabric_minecraft_version}',
            callback.get("getCurTask", lambda _: None)(),
            lambda callback: self.install_minecraft_version(
                fabric_minecraft_version, path, callback=callback
            ),
        )
        task_install_mc.start()
        Task.waitTasks((task_install_mc,), callback)
