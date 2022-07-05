from QtFBN.QFBNWindowManager import QFBNWindowManager
from Ui.Homepage.Homepage import Homepage


class MainWindow(QFBNWindowManager):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Functional Minecraft Launcher")

    def ready(self) -> None:
        self.homepage = Homepage()
        self.homepage.show()
