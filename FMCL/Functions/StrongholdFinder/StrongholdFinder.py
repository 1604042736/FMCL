import math
import os

from Kernel import Kernel
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget
from Setting import Setting

from .ui_StrongholdFinder import Ui_StrongholdFinder


class StrongholdFinder(QWidget, Ui_StrongholdFinder):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(f"{os.path.dirname(__file__)}/ender_eye.png"))

    @pyqtSlot(bool)
    def on_pb_cal_clicked(self, _):
        self.l_error.setText("")
        try:
            # Minecraft以Z轴正方向(南)为0度角,向西偏为正
            # 现在以Z轴正方向为平面直角坐标系X轴正方向
            # X轴正方向为Y轴正方向
            x1 = self.dsb_x1.value()
            z1 = self.dsb_z1.value()
            angle1 = -self.dsb_angle1.value()*math.pi/180
            x2 = self.dsb_x2.value()
            z2 = self.dsb_z2.value()
            angle2 = -self.dsb_angle2.value()*math.pi/180
            # x=k*z+b
            k1 = math.tan(angle1)
            b1 = x1-z1*k1
            k2 = math.tan(angle2)
            b2 = x2-z2*k2
            # k1*z+b1=k2*z+b2
            # =>z=(b2-b1)/(k1-k2)
            z = (b2-b1)/(k1-k2)
            x = k1*z+b1
            self.l_x.setText(f"x: {x}")
            self.l_z.setText(f"z: {z}")
        except Exception as e:
            self.l_error.setText(str(e))

    @pyqtSlot(bool)
    def on_pb_howgetdata_clicked(self, _):
        page = f"{os.path.dirname(__file__)}/howtogetdata_{Setting().get('language.type')}.md"
        Kernel.execFunction("Help", page)
