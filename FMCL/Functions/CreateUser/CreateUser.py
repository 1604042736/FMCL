import qtawesome as qta
from Events import *
from PyQt5.QtCore import pyqtSlot, QEvent
from PyQt5.QtWidgets import QWidget, qApp, QInputDialog
from qfluentwidgets import (
    TransparentToolButton,
    MessageBox,
    TransparentTogglePushButton,
    qconfig,
    isDarkTheme,
)

from Setting import Setting
from Core import YggdrasilAPI
from Core import Function

from .Microsoft import Microsoft
from .Offline import Offline
from .Yggdrasil import Yggdrasil
from .ui_CreateUser import Ui_CreateUser


class CreateUser(QWidget, Ui_CreateUser):
    instance = None
    new_count = 0

    def __new__(cls):
        if CreateUser.instance == None:
            CreateUser.instance = super().__new__(cls)
        CreateUser.new_count += 1
        return CreateUser.instance

    def __init__(self) -> None:
        if CreateUser.new_count > 1:
            return
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(qta.icon("ph.user-circle-plus"))

        self.offline = Offline()
        self.microsoft = Microsoft()

        self.yggdrasil_button: dict[Yggdrasil, TransparentTogglePushButton] = {}

        self.pb_offline.setIcon(self.offline.windowIcon())
        self.pb_microsoft.setIcon(self.microsoft.windowIcon())
        self.pb_addauthlibinjector.setIcon(qta.icon("ri.add-circle-line"))

        self.pb_offline.setChecked(True)
        self.sw_way.addWidget(self.offline)

        self.pb_usermanager = TransparentToolButton()
        functioninfo = Function("UserManager").get_info()
        self.pb_usermanager.setIcon(functioninfo["icon"])
        self.pb_usermanager.resize(46, 32)
        self.pb_usermanager.clicked.connect(lambda: Function("UserManager").exec())

        self.sw_way.currentChanged.connect(self.changePanelState)

        qconfig.themeChanged.connect(self.on_themeChanged)
        self.on_themeChanged()

        self.refresh()

    def on_themeChanged(self):
        self.f_panel.setStyleSheet(
            f"QFrame{{background-color:rgba(255,255,255,{13 if isDarkTheme() else 170})}}"
        )

    def refresh(self):
        while self.vl_yggdrasil.count():
            item = self.vl_yggdrasil.takeAt(0)
            if item.widget() != None:
                item.widget().deleteLater()
        for yggdrasil, _ in self.yggdrasil_button.items():
            yggdrasil.deleteRequest.disconnect(self.deleteAuthlibInjector)

        self.yggdrasil_button = {}
        servers = Setting()["users.authlibinjector_servers"]
        for server in servers:
            button = TransparentTogglePushButton()
            button.setText(server["meta"]["serverName"])
            button.setCheckable(True)
            button.setAutoExclusive(True)

            yggdrasil = Yggdrasil(server)
            yggdrasil.deleteRequest.connect(self.deleteAuthlibInjector)
            self.yggdrasil_button[yggdrasil] = button
            button.clicked.connect(
                lambda _, y=yggdrasil: (
                    self.sw_way.addWidget(y),
                    self.sw_way.setCurrentIndex(self.sw_way.count() - 1),
                )
            )
            self.vl_yggdrasil.addWidget(button)
        self.changePanelState()

    @pyqtSlot(bool)
    def on_pb_offline_clicked(self, _):
        self.sw_way.addWidget(self.offline)
        self.sw_way.setCurrentIndex(self.sw_way.count() - 1)

    @pyqtSlot(bool)
    def on_pb_microsoft_clicked(self, _):
        self.sw_way.addWidget(self.microsoft)
        self.sw_way.setCurrentIndex(self.sw_way.count() - 1)

    @pyqtSlot(bool)
    def on_pb_addauthlibinjector_clicked(self, _):
        url, ok = QInputDialog.getText(
            self, self.tr("添加外置登录"), self.tr("输入认证服务器地址")
        )
        if not ok:
            return
        try:
            api = YggdrasilAPI(url)
            metadata = api.get_metadata()
            servers = Setting()["users.authlibinjector_servers"]
            for server in servers:
                if server["url"] == url:
                    server["meta"] = metadata["meta"]  # 相当于更新元数据
                    Setting().set("users.authlibinjector_servers", servers)
                    break
            else:
                servers.append({"url": url, "meta": metadata["meta"]})
            self.refresh()
        except Exception as e:
            MessageBox(self.tr("无法添加认证服务器"), str(e), self).exec()

    def show(self, tab="offline") -> None:
        super().show()
        if tab == "offline":
            self.pb_offline.click()
        elif tab == "microsoft":
            self.pb_microsoft.click()
        else:
            for yggdrasil, button in self.yggdrasil_button.items():
                if yggdrasil.server["meta"]["serverName"] == tab:
                    button.click()
                    break

    def event(self, a0: QEvent) -> bool:
        if a0.type() == QEvent.Type.Show:
            qApp.sendEvent(self.window(), AddToTitleEvent(self.pb_usermanager, "right"))
            self.refresh()
        elif a0.type() == QEvent.Type.Hide:
            qApp.sendEvent(self.window(), RemoveFromTitleEvent(self.pb_usermanager))
            self.pb_usermanager.setParent(self)
        elif a0.type() == QEvent.Type.WindowActivate:
            self.refresh()
        return super().event(a0)

    def changePanelState(self):
        widget = self.sw_way.currentWidget()
        if widget == None:
            return

        if widget == self.offline:
            self.pb_offline.setChecked(True)
        elif widget == self.microsoft:
            self.pb_microsoft.setChecked(True)
        else:
            for yggdrasil, button in self.yggdrasil_button.items():
                if yggdrasil == widget:
                    button.setChecked(True)
                    break

    def deleteAuthlibInjector(self, widget: Yggdrasil, server: dict):
        def confirmDelete():
            # 保证server是Setting()["users.authlibinjector_servers"]里的元素而不是复制的
            Setting()["users.authlibinjector_servers"].remove(server)
            self.sw_way.removeWidget(widget)
            self.refresh()

        box = MessageBox(
            self.tr("删除认证服务器: ") + server["meta"]["serverName"],
            self.tr("确认删除?"),
            self,
        )
        box.yesSignal.connect(confirmDelete)
        box.exec()
