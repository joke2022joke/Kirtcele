import urllib.request
import webbrowser

from PyQt5.QtWidgets import QLabel, QVBoxLayout, QMenu, QAction, QFrame
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt


class VideoFrame(QFrame):
    def __init__(self, video):
        super().__init__()

        self.video = video

        self.search = True
        self.favorite = False

        self.ui()

    def ui(self):
        width = 200
        height = 150

        self.setLayout(QVBoxLayout())
        self.layout().setAlignment(Qt.AlignTop)
        self.setFixedSize(width, height)
        self.setObjectName('video_frame')

        image_data = urllib.request.urlopen(self.video.img_url).read()
        image = QImage()
        image.loadFromData(image_data)
        image_lbl = QLabel()
        pixmap = QPixmap(image)
        pixmap = pixmap.scaled(180, 80)
        image_lbl.setPixmap(QPixmap(pixmap))

        title = QLabel(f'{self.video.title}')
        title.setFixedHeight(50)
        title.setWordWrap(True)

        self.action_add_to_favorites = QAction('Add to favorites', self)
        self.action_remove_from_favorites = QAction('Remove from favorites', self)

        self.layout().addWidget(image_lbl)
        self.layout().addWidget(title)

        self.setStyleSheet('#video_frame {border: 1px solid black;}')

    def contextMenuEvent(self, event):
        self.context_menu = QMenu(self)

        self.context_menu.addAction(self.action_add_to_favorites)
        self.context_menu.addAction(self.action_remove_from_favorites)

        self.context_menu.actions()[0].setEnabled(self.search)
        self.context_menu.actions()[1].setEnabled(self.favorite)

        action = self.context_menu.exec(self.mapToGlobal(event.pos()))

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            webbrowser.open(self.video.url)


class FavoriteVideoFrame(VideoFrame):
    def __init__(self, video):
        super().__init__(video)

        self.search = False
        self.favorite = True