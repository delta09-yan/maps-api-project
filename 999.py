import os
import sys
import requests
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton
from PyQt6.QtCore import Qt

SCREEN_SIZE = [600, 450]
K = 2

template = '''<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>689</width>
    <height>646</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>MainWindow</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <widget class="QLabel" name="map">
    <property name="geometry">
     <rect>
      <x>0</x>
      <y>0</y>
      <width>671</width>
      <height>521</height>
     </rect>
    </property>
    <property name="text">
     <string/>
    </property>
   </widget>
   <widget class="QPushButton" name="theme_button">
    <property name="geometry">
     <rect>
      <x>280</x>
      <y>530</y>
      <width>150</width>
      <height>30</height>
     </rect>
    </property>
    <property name="text">
     <string>Темная тема</string>
    </property>
   </widget>
  </widget>
  <widget class="QStatusBar" name="statusbar"/>
 </widget>
 <resources/>
 <connections/>
</ui>
'''


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ll = [37.530887, 55.703118]
        self.spn = [0.005, 0.005]
        self.theme = 'light'
        self.map_file = "map.png"

        self.initUI()
        self.getImage()
        self.update_picture()

    def initUI(self):
        self.setGeometry(100, 100, 689, 600)
        self.setWindowTitle('Отображение карты')

        self.image = QLabel(self)
        self.image.setGeometry(0, 0, 671, 521)

        self.theme_button = QPushButton('Темная тема', self)
        self.theme_button.setGeometry(280, 530, 150, 30)
        self.theme_button.clicked.connect(self.change_theme)

    def getImage(self):
        server = 'https://static-maps.yandex.ru/v1?'
        api_key = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'
        ll_str = f"{self.ll[0]},{self.ll[1]}"
        spn_str = f"{self.spn[0]},{self.spn[1]}"

        if self.theme == 'dark':
            theme_param = '&theme=dark'
        else:
            theme_param = ''

        request = f"{server}ll={ll_str}&spn={spn_str}{theme_param}&apikey={api_key}"

        response = requests.get(request)
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def update_picture(self):
        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)
        self.image.setScaledContents(True)

    def change_theme(self):
        if self.theme == 'light':
            self.theme = 'dark'
            self.theme_button.setText('Светлая тема')
        else:
            self.theme = 'light'
            self.theme_button.setText('Темная тема')
        self.getImage()
        self.update_picture()

    def closeEvent(self, event):
        if os.path.exists(self.map_file):
            os.remove(self.map_file)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Right:
            self.ll = [self.ll[0] + 0.001000, self.ll[1]]
            self.getImage()
            self.update_picture()
        if event.key() == Qt.Key.Key_Left:
            self.ll = [self.ll[0] - 0.001000, self.ll[1]]
            self.getImage()
            self.update_picture()
        if event.key() == Qt.Key.Key_Up:
            self.ll = [self.ll[0], self.ll[1] + 0.001000]
            self.getImage()
            self.update_picture()
        if event.key() == Qt.Key.Key_Down:
            self.ll = [self.ll[0], self.ll[1] - 0.001000]
            self.getImage()
            self.update_picture()
        if event.key() == Qt.Key.Key_PageUp:
            self.spn = [self.spn[0] * K, self.spn[1] * K]
            self.getImage()
            print(self.spn)
            self.update_picture()
        if event.key() == Qt.Key.Key_PageDown:
            self.spn = [self.spn[0] / K, self.spn[1] / K]
            self.getImage()
            print(self.spn)
            self.update_picture()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())