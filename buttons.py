import os
import sys
import requests
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QWidget, QLabel
from PyQt6.QtCore import Qt

SCREEN_SIZE = [600, 450]
K = 2
MIN_SPN = 0.0001
MAX_SPN = 90.0
MOVE_STEP_COEFF = 0.1


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.ll = [37.530887, 55.703118]
        self.spn = [0.005, 0.005]
        self.getImage(self.ll, self.spn)
        self.initUI()


    def getImage(self, ll, spn):
        help_list = ','.join([str(i) for i in ll])
        help_list_spn = ','.join([str(i) for i in spn])
        server_address = 'https://static-maps.yandex.ru/v1?'
        api_key = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'
        ll_spn = f'll={help_list}&spn={help_list_spn}'
        # Готовим запрос.

        map_request = f"{server_address}{ll_spn}&apikey={api_key}"
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

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')

        ## Изображение
        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.image.setPixmap(self.pixmap)

    def update_picture(self):
        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)

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


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    sys.excepthook = except_hook
    ex = Example()
    ex.show()
    sys.exit(app.exec())
