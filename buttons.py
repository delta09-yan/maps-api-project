import os
import sys
import io
import requests
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QMainWindow
from PyQt6.QtCore import Qt
from PyQt6 import uic

SCREEN_SIZE = [600, 450]
K = 2
MIN_SPN = 0.0001
MAX_SPN = 90.0
MOVE_STEP_COEFF = 0.1
template = '''<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>614</width>
    <height>584</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>MainWindow</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <widget class="QLabel" name="map">
    <property name="geometry">
     <rect>
      <x>10</x>
      <y>0</y>
      <width>791</width>
      <height>521</height>
     </rect>
    </property>
    <property name="text">
     <string/>
    </property>
   </widget>
   <widget class="QPushButton" name="light">
    <property name="geometry">
     <rect>
      <x>10</x>
      <y>530</y>
      <width>111</width>
      <height>23</height>
     </rect>
    </property>
    <property name="text">
     <string>Темная тема</string>
    </property>
   </widget>
   <widget class="QLineEdit" name="text_edit">
    <property name="geometry">
     <rect>
      <x>462</x>
      <y>530</y>
      <width>121</width>
      <height>20</height>
     </rect>
    </property>
    <property name="text">
     <string/>
    </property>
   </widget>
   <widget class="QPushButton" name="search">
    <property name="geometry">
     <rect>
      <x>370</x>
      <y>530</y>
      <width>75</width>
      <height>23</height>
     </rect>
    </property>
    <property name="text">
     <string>Поиск</string>
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
        f = io.StringIO(template)
        uic.loadUi(f, self)
        self.ll = [37.530887, 55.703118]
        self.spn = [0.005, 0.005]
        self.theme = 'light'
        self.pts = []
        self.getImage(self.ll, self.spn)
        self.setWindowTitle('Отображение карты')
        self.pixmap = QPixmap(self.map_file)
        self.map.setPixmap(self.pixmap)
        self.light.clicked.connect(self.changetheme)
        self.setFocus()
        self.search.clicked.connect(self.search_address)


    def getImage(self, ll, spn):
        help_list = ','.join([str(i) for i in ll])
        help_list_spn = ','.join([str(i) for i in spn])
        server_address = 'https://static-maps.yandex.ru/v1?'
        api_key = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'
        ll_spn = f'll={help_list}&spn={help_list_spn}'
        # Готовим запрос.

        map_request = f"{server_address}{ll_spn}&apikey={api_key}&theme={self.theme}"
        if self.pts != []:
            pts = '~'.join([f"{coord[0]},{coord[1]},pm2rdm" for coord in self.pts])
            map_request += f'&pt={pts}'
        response = requests.get(map_request)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        # Запишем полученное изображение в файл.
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def update_picture(self):
        self.pixmap = QPixmap(self.map_file)
        self.map.setPixmap(self.pixmap)
        self.setFocus()

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)

    def keyPressEvent(self, event):
        move_step = max(self.spn[0], self.spn[1]) * MOVE_STEP_COEFF
        if event.key() == Qt.Key.Key_Right:
            self.ll = [self.ll[0] + move_step, self.ll[1]]
            self.getImage(self.ll, self.spn)
            self.update_picture()
        if event.key() == Qt.Key.Key_Left:
            self.ll = [self.ll[0] - move_step, self.ll[1]]
            self.getImage(self.ll, self.spn)
            self.update_picture()
        if event.key() == Qt.Key.Key_Up:
            self.ll = [self.ll[0], self.ll[1] + move_step]
            self.getImage(self.ll, self.spn)
            self.update_picture()
        if event.key() == Qt.Key.Key_Down:
            self.ll = [self.ll[0], self.ll[1] - move_step]
            self.getImage(self.ll, self.spn)
            self.update_picture()
        if event.key() == Qt.Key.Key_PageUp:
            new_spn_lon = self.spn[0] * K
            new_spn_lat = self.spn[1] * K
            if new_spn_lon <= MAX_SPN and new_spn_lat <= MAX_SPN:
                self.spn = [new_spn_lon, new_spn_lat]
                self.getImage(self.ll, self.spn)
                self.update_picture()
            else:
                pass
        if event.key() == Qt.Key.Key_PageDown:
            new_spn_lon = self.spn[0] / K
            new_spn_lat = self.spn[1] / K
            if new_spn_lon >= MIN_SPN and new_spn_lat >= MIN_SPN:
                self.spn = [new_spn_lon, new_spn_lat]
                self.getImage(self.ll, self.spn)
                print(self.spn)
                self.update_picture()
            else:
                pass

    def changetheme(self):
        if self.theme == 'light':
            self.theme = 'dark'
            self.light.setText('Светлая тема')
            self.getImage(self.ll, self.spn)
            self.update_picture()
            self.setFocus()
        else:
            self.theme = 'light'
            self.light.setText('Темная тема')
            self.getImage(self.ll, self.spn)
            self.update_picture()
            self.setFocus()

    def search_address(self):
        if self.text_edit.text():
            api_key = '8013b162-6b42-4997-9691-77b7074026e0'
            server_address = 'http://geocode-maps.yandex.ru/1.x/?'
            geocoder_request = f'{server_address}apikey={api_key}&geocode={self.text_edit.text()}&format=json'
            # Выполняем запрос.
            response = requests.get(geocoder_request)
            if response:
                # Преобразуем ответ в json-объект
                json_response = response.json()
                geocode = list(map(float, json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]['Point'][
                    "pos"].split()))
                self.pts.append(geocode)
                self.ll = geocode
                self.getImage(self.ll, self.spn)
                self.update_picture()
                self.setFocus()

            else:
                print("Ошибка выполнения запроса:")
                print(geocoder_request)
                print("Http статус:", response.status_code, "(", response.reason, ")")




def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sys.excepthook = except_hook
    ex = Example()
    ex.show()
    sys.exit(app.exec())
