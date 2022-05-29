from api.youtube import *
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QLabel, QFrame
from PyQt5.QtCore import Qt

from db import database
from .video_frames import VideoFrame, FavoriteVideoFrame
from .utils import log_in, get_favorites_videos


class LoginWindow(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = uic.loadUi('gui/StartWindow.ui')
        self.ui.setFixedSize(1200, 800)

        self.ui.login_btn.clicked.connect(self.login_btn_pressed)

        self.ui.actionNext.triggered.connect(self.login_btn_pressed)
        self.ui.actionQuit.triggered.connect(self.ui.close)

        self.ui.show()

    def login_btn_pressed(self):
        if self.ui.username_le.text():
            username = self.ui.username_le.text()
            log_in(username)

            self.ui = MainWindow(username)
        else:
            self.ui.statusbar.showMessage('Username is not correct')


class MainWindow(QWidget):
    USER_REGION = "UA"

    def __init__(self, username, parent=None):
        super().__init__(parent)

        self.username = username

        self.ui = uic.loadUi('gui/MainWindow.ui')
        self.ui.setFixedSize(1200, 800)

        self.ui.trends_lbl.setFixedHeight(50)
        self.ui.favorites_lbl.setFixedHeight(50)

        # Creating labels for status bar
        self.statusLeft = QLabel('Favorites column')
        self.statusMiddle = QLabel('On Trends column')
        self.statusRight = QLabel('Search column')

        self.ui.favorites_contents.layout().setAlignment(Qt.AlignTop)
        self.ui.search_contents.layout().setAlignment(Qt.AlignTop)
        self.ui.trends_contents.layout().setAlignment(Qt.AlignTop)

        # Setting frame style and alignment for labels
        self.statusLeft.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.statusLeft.setAlignment(Qt.AlignHCenter)
        self.statusMiddle.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.statusMiddle.setAlignment(Qt.AlignHCenter)
        self.statusRight.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.statusRight.setAlignment(Qt.AlignHCenter)

        # Adding labels to status bar
        self.ui.statusbar.addPermanentWidget(self.statusLeft, 1)
        self.ui.statusbar.addPermanentWidget(self.statusMiddle, 1)
        self.ui.statusbar.addPermanentWidget(self.statusRight, 1)

        self.ui.search_le.setPlaceholderText('Search')
        self.ui.setStyleSheet('#search_btn, #trends_lbl, #favorites_lbl {border: 1px solid black;}')

        self.fill_favorites()
        self.fill_trends()

        self.ui.back_btn.clicked.connect(self.back_btn_pressed)
        self.ui.search_btn.clicked.connect(self.search_btn_pressed)

        self.ui.actionBack.triggered.connect(self.back_btn_pressed)
        self.ui.actionSearch.triggered.connect(self.search_btn_pressed)
        self.ui.actionQuit.triggered.connect(self.ui.close)

        self.ui.show()

    def fill_favorites(self):
        video_tuples = get_favorites_videos(self.username)
        for t in video_tuples:
            video = Video()
            video.title = t[2]
            video.url = t[3]
            video.img_url = t[4]

            frame = FavoriteVideoFrame(video)
            frame.action_remove_from_favorites.triggered.connect(lambda state, f=frame: self.remove_from_favorites(f))
            self.ui.favorites_contents.layout().addWidget(frame)

    def fill_trends(self):
        video_trends_dict = videos_popular(self.USER_REGION, 3)
        for video in video_trends_dict:
            frame = VideoFrame(video)
            frame.action_add_to_favorites.triggered.connect(lambda state, f=frame: self.add_to_favorites(f))
            self.ui.trends_contents.layout().addWidget(frame)
            self.statusMiddle.setText('Successful filling "On Trends"')

    def fill_search(self, txt):
        videos_dict = videos_by_string(txt, 3)
        for video in videos_dict:
            frame = VideoFrame(video)
            frame.action_add_to_favorites.triggered.connect(lambda state, f=frame: self.add_to_favorites(f))
            self.ui.search_contents.layout().addWidget(frame)
            self.statusRight.setText('Successful search')

    def add_to_favorites(self, frame):
        database.add_favorite_video(self.username, frame.video.title, frame.video.url, frame.video.img_url)

        video = FavoriteVideoFrame(frame.video)

        duplicate_check = False
        for i in self.ui.favorites_contents.findChildren(FavoriteVideoFrame):
            if video.video.url == i.video.url:
                duplicate_check = True
                break
        if not duplicate_check:
            video.action_remove_from_favorites.triggered.connect(lambda state, f=frame: self.remove_from_favorites(f))
            self.ui.favorites_contents.layout().addWidget(video)
        self.statusLeft.setText('Successfully added to favorites')

    def remove_from_favorites(self, frame):
        database.delete_favorite_video(frame.video.title, self.username)

        for i in self.ui.favorites_contents.findChildren(FavoriteVideoFrame):
            if i.video.url == frame.video.url:
                i.setParent(None)
                self.ui.search_contents.layout().removeWidget(i)
        self.statusLeft.setText('Successfully removed from favorites')

    def back_btn_pressed(self):
        self.ui = LoginWindow()

    def search_btn_pressed(self):
        for i in self.ui.search_contents.findChildren(VideoFrame):
            i.setParent(None)
            self.ui.search_contents.layout().removeWidget(i)

        if self.ui.search_le.text():
            self.fill_search(self.ui.search_le.text())
