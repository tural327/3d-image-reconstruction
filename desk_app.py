from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from PyQt5.QtGui import QImage
import cv2
from PyQt5.QtGui import QFont,QPixmap
from PyQt5.QtCore import QTimer
import sys
from my3d import my_3d_func
import os
import matplotlib.pyplot as plt
a = ["test"]


class Main_space(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('3d image reconstruction')
        self.setFixedWidth(1200)
        self.setFixedHeight(700)

        self.timer = QTimer()
# camera display
        self.timer.timeout.connect(self.viewCam)
        self.pixmap = QPixmap("camera_display.jpg")
        self.main_display = QtWidgets.QLabel(self)
        self.main_display.setPixmap(self.pixmap)
        self.main_display.setScaledContents(True)
        self.main_display.setGeometry(100,150,600,400)
        self.main_display.move(10,10)
# Camera button
        self.dis_change = QPushButton("Start", self)
        self.dis_change.setStyleSheet("background-color : red")
        self.dis_change.pressed.connect(self.controlTimer)
        self.dis_change.setGeometry(100, 200, 200, 30)
        self.dis_change.move(50, 460)
# first image
        self.first_img_text = QtWidgets.QLabel(self)
        self.first_img_text.setText("Image 1")
        self.first_img_text.setFont(QFont("Times", 13))
        self.first_img_text.setGeometry(0, 50, 200, 25)
        self.first_img_text.move(900, 5)
# import first images
        self.first_img_file = QPixmap("t1.png")
        self.first_img_display = QtWidgets.QLabel(self)
        self.first_img_display.setPixmap(self.first_img_file)
        self.first_img_display.setScaledContents(True)
        self.first_img_display.setGeometry(100, 150, 400, 300)
        self.first_img_display.move(700, 30)

## Second image

        self.second_img_text = QtWidgets.QLabel(self)
        self.second_img_text.setText("Image 2")
        self.second_img_text.setFont(QFont("Times", 13))
        self.second_img_text.setGeometry(0, 50, 200, 25)
        self.second_img_text.move(900, 330)
# Second image
        self.second_img_file = QPixmap("t2.png")
        self.second_img_display = QtWidgets.QLabel(self)
        self.second_img_display.setPixmap(self.second_img_file)
        self.second_img_display.setScaledContents(True)
        self.second_img_display.setGeometry(100, 150, 400, 300)
        self.second_img_display.move(700, 360)
    # Adding 3d maker button
        self.make_3d = QPushButton("Make my 3D", self)
        self.make_3d.setStyleSheet("background-color : green")
        self.make_3d.pressed.connect(self.make_3d_plot)
        self.make_3d.setGeometry(100, 200, 200, 30)
        self.make_3d.move(200, 560)
    # Take first image
        self.first_img_camera = QPushButton("Take my first image", self)
        self.first_img_camera.pressed.connect(self.img_1)
        self.first_img_camera.setGeometry(100, 200, 200, 30)
        self.first_img_camera.move(400, 460)
    # Delete first image
        self.first_img_delete = QPushButton("Delete my first image", self)
        self.first_img_delete.pressed.connect(self.delete_img1)
        self.first_img_delete.setGeometry(100, 200, 200, 30)
        self.first_img_delete.move(400, 460)
        self.first_img_delete.hide()
    # Take second image
        self.second_img_camera = QPushButton("Take my second image", self)
        self.second_img_camera.pressed.connect(self.img_2)
        self.second_img_camera.setGeometry(100, 200, 200, 30)
        self.second_img_camera.move(400, 500)
    # Delete second image
        self.second_img_delete = QPushButton("Delete my second image", self)
        self.second_img_delete.pressed.connect(self.delete_img2)
        self.second_img_delete.setGeometry(100, 200, 200, 30)
        self.second_img_delete.move(400, 500)
        self.second_img_delete.hide()

# function for controlling camera start and stop
    def viewCam(self):
        ret, image = self.cap.read()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        height, width, channel = image.shape
        step = channel * width
        qImg = QImage(image.data, width, height, step, QImage.Format_RGB888)
        self.main_display.setPixmap(QPixmap.fromImage(qImg))
        self.main_display.setScaledContents(True)
        a[0] = image

    def controlTimer(self):
        # if timer is stopped
        if not self.timer.isActive():
            # create video capture
            self.cap = cv2.VideoCapture(0)
            # start timer
            self.timer.start(20)
            # update control_bt text
            self.dis_change.setText("Stop")
        else:
            self.pixmap = QPixmap("camera_display.jpg")
            self.main_display.setPixmap(self.pixmap)
            self.timer.stop()
            self.cap.release()
            self.dis_change.setText("Start")

    def make_3d_plot(self):
        try:
            X , Y , Z = my_3d_func("img1.jpg","img2.jpg")
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            ax.scatter(X, Y, Z, c='r', marker='o')
            plt.show()
            print("my_photo")
        except:
            X , Y , Z = my_3d_func("t1.png","t1.png")
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            ax.scatter(X, Y, Z, c='r', marker='o')
            plt.show()
            print("main")
    # my first image save
    def img_1(self):
        try:
            save_img1 = cv2.cvtColor(a[0], cv2.COLOR_BGR2RGB)
            cv2.imwrite("img1.jpg",save_img1)
            self.img1 = QPixmap("img1.jpg")
            self.first_img_display.setPixmap(self.img1)
            self.first_img_display.setScaledContents(True)
            self.first_img_camera.hide()
            self.first_img_delete.show()
        except:
            None

    #my first image delete
    def delete_img1(self):
        os.remove("img1.jpg")
        self.first_img_file = QPixmap("t1.png")
        self.first_img_display.setPixmap(self.first_img_file)
        self.first_img_display.setScaledContents(True)
        self.first_img_camera.show()
        self.first_img_delete.hide()

    def img_2(self):
        try:
            save_img1 = cv2.cvtColor(a[0], cv2.COLOR_BGR2RGB)
            cv2.imwrite("img2.jpg",save_img1)
            self.img2 = QPixmap("img2.jpg")
            self.second_img_display.setPixmap(self.img2)
            self.second_img_display.setScaledContents(True)
            self.second_img_camera.hide()
            self.second_img_delete.show()
        except:
            None

    #my first image delete
    def delete_img2(self):
        os.remove("img2.jpg")
        self.second_img_file = QPixmap("t2.png")
        self.second_img_display.setPixmap(self.second_img_file)
        self.second_img_display.setScaledContents(True)
        self.second_img_camera.show()
        self.second_img_delete.hide()





if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main_space()
    ex.show()
    app.exec_()
