import os
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QEvent
from PyQt5.QtWidgets import QFileDialog, QLabel, QWidget, QInputDialog

from Setting import Setting
from Core import (
    ModrinthVersionModel,
    ModrinthAPI,
    ModrinthVersionFile,
    ModrinthProjectModel,
    Task,
    Download,
    Version,
)

from .VersionItem import VersionItem


class ModrinthVersionItem(VersionItem):
    showDependenciesRequest = pyqtSignal(QWidget)  # 请求显示依赖

    def __init__(self, version: ModrinthVersionModel, project: ModrinthProjectModel):
        super().__init__(version)
        self.project = project
        self.l_name.setText(version["name"])

        self.api = ModrinthAPI()
        translations = self.api.get_translations()

        info = []

        info.append(translations[version["version_type"]])
        info.append(f'{self.tr("下载量")}: {version["downloads"]}')
        info.append(f'{self.tr("发布")}: {self.api.get_time(version["date_published"])}')
        info.append(f'{self.tr("加载器")}: {"|".join(version["loaders"])}')
        info.append(f'{self.tr("适用版本")}: {"|".join(version["game_versions"])}')

        self.l_info.setText(", ".join(info))

        if version["dependencies"]:
            label = QLabel()
            label.setText(self.tr("双击查看依赖"))
            label.setStyleSheet(
                """
QLabel{
    background-color:rbg(200,200,200);
    border:1px solid black;
}
"""
            )
            self.hl_label.addWidget(label)

    @pyqtSlot(bool)
    def on_pb_download_clicked(self, _):
        file: ModrinthVersionFile = self.api.get_primary_file(self.version)
        url = file["url"]
        filename = file["filename"]
        path = QFileDialog.getSaveFileName(self, self.tr("下载"), f"./{filename}")[0]
        if path:
            Task(
                self.tr("下载") + filename,
                taskfunc=lambda callback: Download(url, path, callback).start(),
            ).start()

    @pyqtSlot(bool)
    def on_pb_install_clicked(self, _):
        project_type = self.project["project_type"]
        if project_type != "modpack":
            version_dir = os.path.join(Setting()["game.directories"][0], "versions")
            name, ok = QInputDialog.getItem(
                self,
                self.tr("选择安装到哪个版本"),
                "",
                [
                    i
                    for i in os.listdir(version_dir)
                    if os.path.isdir(os.path.join(version_dir, i))
                ],
                editable=False,
            )
            if not ok:
                return
        file = self.api.get_primary_file(self.version)
        if project_type == "mod":
            Version(name).install_mod(file["url"], file["filename"])
        elif project_type == "resourcepack":
            Version(name).install_resourcepack(file["url"], file["filename"])
        elif project_type == "shader":
            Version(name).install_shaderpack(file["url"], file["filename"])
        elif project_type == "modpack":
            name, ok = QInputDialog.getText(
                self, self.tr("输入版本名"), "", text=self.project["title"]
            )
            if not ok:
                return
            Version(name).install_modpack(file["url"], file["filename"])

    def event(self, a0: QEvent | None) -> bool:
        if a0.type() == QEvent.Type.MouseButtonDblClick:
            self.showDependenciesRequest.emit(self)
        return super().event(a0)
