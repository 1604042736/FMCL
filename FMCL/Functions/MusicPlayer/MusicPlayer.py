import qtawesome as qta
from Events import *
from Kernel import Kernel
from PyQt5.QtCore import QUrl, pyqtSlot, QEvent
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer, QMediaPlaylist
from PyQt5.QtWidgets import QFileDialog, QListWidgetItem, QWidget, qApp
from qfluentwidgets import MessageBox, TransparentToolButton
from Setting import Setting

from .ui_MusicPlayer import Ui_MusicPlayer


class MusicPlayer(QWidget, Ui_MusicPlayer):
    instance = None
    new_count = 0

    def __new__(cls):
        if MusicPlayer.instance == None:
            MusicPlayer.instance = super().__new__(cls)
        MusicPlayer.new_count += 1
        return MusicPlayer.instance

    def __init__(self) -> None:
        if MusicPlayer.new_count > 1:
            return
        super().__init__()
        self.setWindowIcon(qta.icon("ei.music"))
        self.setupUi(self)

        self.pb_add.setIcon(qta.icon("msc.add"))
        self.pb_remove.setIcon(qta.icon("msc.remove"))
        self.pb_movedown.setIcon(qta.icon("fa5s.arrow-down"))
        self.pb_moveup.setIcon(qta.icon("fa5s.arrow-up"))
        self.pb_movetop.setIcon(qta.icon("mdi.arrow-collapse-up"))
        self.pb_pre.setIcon(qta.icon("fa5s.arrow-left"))
        self.pb_next.setIcon(qta.icon("fa5s.arrow-right"))
        self.pb_control.setIcon(qta.icon("fa.play"))

        self.pb_gosetting = TransparentToolButton()
        self.pb_gosetting.setIcon(qta.icon("ri.settings-5-line"))
        self.pb_gosetting.resize(46, 32)
        self.pb_gosetting.clicked.connect(
            lambda: Kernel.execFunction("SettingEditor", id="musicplayer")
        )

        self.pb_refresh = TransparentToolButton()
        self.pb_refresh.resize(46, 32)
        self.pb_refresh.setIcon(qta.icon("mdi.refresh"))
        self.pb_refresh.clicked.connect(lambda: self.refresh())

        self.pb_music = TransparentToolButton()
        self.pb_music.resize(46, 32)
        self.pb_music.setIcon(qta.icon("ei.music"))
        self.pb_music.clicked.connect(lambda: Kernel.execFunction("MusicPlayer"))

        setting = Setting()
        self.playlist = QMediaPlaylist(self)
        self.player = QMediaPlayer(self)
        self.player.currentMediaChanged.connect(self.setMusicName)
        self.player.positionChanged.connect(self.setMusicTime)
        self.player.durationChanged.connect(self.setMusicTime)
        self.player.stateChanged.connect(self.setButton)
        self.hs_music.sliderMoved.connect(self.player.setPosition)
        self.player.setPlaylist(self.playlist)
        self.player.setVolume(setting["musicplayer.volume"])
        self.hs_sound.setValue(setting["musicplayer.volume"])
        self.playlist.currentIndexChanged.connect(self.syncStartIndex)
        self.playlist.setPlaybackMode(QMediaPlaylist.PlaybackMode.Loop)
        self.playlist.setCurrentIndex(setting["musicplayer.startindex"])

        for i in setting["musicplayer.musiclist"]:
            self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(i)))

    def refresh(self):
        musiclist = []
        self.lw_musiclist.clear()
        for i in range(self.playlist.mediaCount()):
            media = self.playlist.media(i)
            music = media.canonicalUrl().url(QUrl.UrlFormattingOption.PreferLocalFile)
            self.lw_musiclist.addItem(music)
            musiclist.append(music)
        Setting().set("musicplayer.musiclist", musiclist)
        self.hs_sound.setValue(Setting()["musicplayer.volume"])

    def event(self, a0: QEvent) -> bool:
        if a0.type() == QEvent.Type.Show:
            qApp.sendEvent(self.window(), AddToTitleEvent(self.pb_gosetting, "right"))
            qApp.sendEvent(self.window(), AddToTitleEvent(self.pb_refresh, "right"))
            self.refresh()
        elif a0.type() == QEvent.Type.Hide:
            qApp.sendEvent(self.window(), RemoveFromTitleEvent(self.pb_gosetting))
            qApp.sendEvent(self.window(), RemoveFromTitleEvent(self.pb_refresh))
            self.pb_gosetting.setParent(self)
            self.pb_refresh.setParent(self)
        return super().event(a0)

    @pyqtSlot(bool)
    def on_pb_add_clicked(self, _):
        files, _ = QFileDialog.getOpenFileNames(
            self, self.tr("选择音频文件"), ".", "Sound(*wav *.mp3)"
        )
        for file in files:
            self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(file)))
        self.refresh()

    @pyqtSlot(bool)
    def on_pb_remove_clicked(self, _):
        if not self.lw_musiclist.currentItem():
            return
        index = self.lw_musiclist.currentRow()

        def confirmDeleted():
            self.playlist.removeMedia(index)
            self.refresh()

        box = MessageBox("", self.tr("确认删除") + "?", self.window())
        box.yesSignal.connect(confirmDeleted)
        box.exec()

    @pyqtSlot(bool)
    def on_pb_moveup_clicked(self, _):
        if not self.lw_musiclist.currentItem():
            return
        index = self.lw_musiclist.currentRow()
        if index != 0:
            self.playlist.moveMedia(index, index - 1)
        self.refresh()

    @pyqtSlot(bool)
    def on_pb_movedown_clicked(self, _):
        if not self.lw_musiclist.currentItem():
            return
        index = self.lw_musiclist.currentRow()
        if index != self.playlist.mediaCount() - 1:
            self.playlist.moveMedia(index, index + 1)
        self.refresh()

    @pyqtSlot(bool)
    def on_pb_movetop_clicked(self, _):
        if not self.lw_musiclist.currentItem():
            return
        index = self.lw_musiclist.currentRow()
        self.playlist.moveMedia(index, 0)
        self.refresh()

    @pyqtSlot(bool)
    def on_pb_control_clicked(self, _):
        if self.player.state() == QMediaPlayer.State.PlayingState:
            self.player.pause()
        else:
            self.player.play()

    @pyqtSlot(int)
    def on_hs_sound_valueChanged(self, value):
        self.player.setVolume(value)
        Setting().set("musicplayer.volume", value)

    @pyqtSlot(bool)
    def on_pb_next_clicked(self, _):
        self.playlist.next()

    @pyqtSlot(bool)
    def on_pb_pre_clicked(self, _):
        self.playlist.previous()

    @pyqtSlot(QListWidgetItem)
    def on_lw_musiclist_itemDoubleClicked(self, item):
        self.playlist.setCurrentIndex(self.lw_musiclist.row(item))
        self.player.play()

    def setMusicName(self):
        media = self.player.currentMedia()
        self.l_musicname.setText(
            media.canonicalUrl().url(QUrl.UrlFormattingOption.PreferLocalFile)
        )

    def setMusicTime(self):
        def totime(a):
            s = a // 1000 % 60
            m = a // 1000 // 60
            return f"{m}:{s}"

        p = self.player.position()
        d = self.player.duration()
        self.hs_music.setRange(0, d)
        self.hs_music.setValue(p)
        self.l_time.setText(f"{totime(p)}/{totime(d)}")

    def setButton(self, state):
        if state == QMediaPlayer.State.PlayingState:
            self.pb_control.setIcon(qta.icon("mdi6.pause"))
            qApp.sendEvent(
                qApp.topLevelWindows()[0], AddToTitleEvent(self.pb_music, "right")
            )
            self.pb_music.show()
        else:
            self.pb_control.setIcon(qta.icon("fa.play"))
            qApp.sendEvent(
                qApp.topLevelWindows()[0], RemoveFromTitleEvent(self.pb_music)
            )
            self.pb_music.hide()

    def syncStartIndex(self, i):
        setting = Setting()
        if setting["musicplayer.auto_sync_startindex"]:
            setting.set("musicplayer.startindex", i)
