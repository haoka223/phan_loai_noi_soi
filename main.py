import os
import sys

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from ui_app import Ui_MainWindow

import pymongo

os.environ.update({"QT_QPA_PLATFORM_PLUGIN_PATH": "C:/Users/ADMIN/AppData/Local/Programs/Python/Python310/Lib/site-packages/PySide2/plugins"})

filepath = 0
filename = 1
category = 2
noiserate = 3
blur = 4
overexposure = 5
dark = 6
fluid = 7


def openFolder():
    dir_ = os.getcwd()
    dir_ = QFileDialog.getExistingDirectory(None, 'Select a folder', dir_, QFileDialog.ShowDirsOnly)

    if dir_ != '':
        return str(dir_)
    else:
        return None


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client["endo"]

        self.disableScoreOption()
        self.disableNoiseOption()

        self.ui.actionOpen_folder.triggered.connect(self.btn_actionOpen_folderIsClicked)

        self.ui.btn_next.clicked.connect(self.nextImage)
        self.ui.btn_back.clicked.connect(self.backImage)

        self.ui.btn_25.clicked.connect(self.btn25Clicked)
        self.ui.btn_50.clicked.connect(self.btn50Clicked)
        self.ui.btn_75.clicked.connect(self.btn75Clicked)
        self.ui.btn_100.clicked.connect(self.btn100Clicked)
        self.ui.btn_info.clicked.connect(self.btnInfoClicked)
        self.ui.btn_noninfo.clicked.connect(self.btnNonInfoClicked)

        self.ui.listWidget.itemClicked.connect(self.chooseNoiseImage)
        self.ui.listWidget_2.itemClicked.connect(self.chooseCleanImage)

        self.showMaximized()

    def disableScoreOption(self):
        self.ui.btn_25.setCheckable(False)
        self.ui.btn_50.setCheckable(False)
        self.ui.btn_75.setCheckable(False)
        self.ui.btn_100.setCheckable(False)
        self.ui.btn_info.setCheckable(False)
        self.ui.btn_noninfo.setCheckable(False)

    def enableScoreOption(self):
        self.ui.btn_25.setCheckable(True)
        self.ui.btn_50.setCheckable(True)
        self.ui.btn_75.setCheckable(True)
        self.ui.btn_100.setCheckable(True)
        self.ui.btn_info.setCheckable(True)
        self.ui.btn_noninfo.setCheckable(True)

    def disableNoiseOption(self):
        self.ui.btn_blur.setChecked(False)
        self.ui.btn_over.setChecked(False)
        self.ui.btn_dark.setChecked(False)
        self.ui.btn_fluid.setChecked(False)
        self.ui.btn_blur.setCheckable(False)
        self.ui.btn_over.setCheckable(False)
        self.ui.btn_dark.setCheckable(False)
        self.ui.btn_fluid.setCheckable(False)

    def enableNoiseOption(self):
        self.ui.btn_blur.setCheckable(True)
        self.ui.btn_over.setCheckable(True)
        self.ui.btn_dark.setCheckable(True)
        self.ui.btn_fluid.setCheckable(True)

    def btn25Clicked(self):
        if self.ui.btn_25.isChecked():
            self.ui.btn_50.setChecked(False)
            self.ui.btn_75.setChecked(False)
            self.ui.btn_100.setChecked(False)
            self.ui.btn_info.setChecked(False)
            self.ui.btn_noninfo.setChecked(False)
            self.enableNoiseOption()
        else:
            self.disableNoiseOption()

    def btn50Clicked(self):
        if self.ui.btn_50.isChecked():
            self.ui.btn_25.setChecked(False)
            self.ui.btn_75.setChecked(False)
            self.ui.btn_100.setChecked(False)
            self.ui.btn_info.setChecked(False)
            self.ui.btn_noninfo.setChecked(False)
            self.enableNoiseOption()
        else:
            self.disableNoiseOption()

    def btn75Clicked(self):
        if self.ui.btn_75.isChecked():
            self.ui.btn_25.setChecked(False)
            self.ui.btn_50.setChecked(False)
            self.ui.btn_100.setChecked(False)
            self.ui.btn_info.setChecked(False)
            self.ui.btn_noninfo.setChecked(False)
            self.enableNoiseOption()
        else:
            self.disableNoiseOption()

    def btn100Clicked(self):
        if self.ui.btn_100.isChecked():
            self.ui.btn_25.setChecked(False)
            self.ui.btn_50.setChecked(False)
            self.ui.btn_75.setChecked(False)
            self.ui.btn_info.setChecked(False)
            self.ui.btn_noninfo.setChecked(False)
            self.enableNoiseOption()
        else:
            self.disableNoiseOption()

    def btnInfoClicked(self):
        if self.ui.btn_info.isChecked():
            self.ui.btn_25.setChecked(False)
            self.ui.btn_50.setChecked(False)
            self.ui.btn_75.setChecked(False)
            self.ui.btn_100.setChecked(False)
            self.ui.btn_noninfo.setChecked(False)
            self.disableNoiseOption()

    def btnNonInfoClicked(self):
        if self.ui.btn_noninfo.isChecked():
            self.ui.btn_25.setChecked(False)
            self.ui.btn_50.setChecked(False)
            self.ui.btn_75.setChecked(False)
            self.ui.btn_100.setChecked(False)
            self.ui.btn_info.setChecked(False)
            self.disableNoiseOption()

    def btn_actionOpen_folderIsClicked(self):
        self.folder_path = openFolder()

        if self.folder_path is not None:
            loadDir = QDir(self.folder_path)
            loadDir.setNameFilters(['*.jpg', '*.JPG', '*.png', '*.PNG', '*.jpeg', '*.JPEG'])
            self.infoList = loadDir.entryInfoList()

            self.listImageData = []
            self.currentId = 0
            self.collection = self.db[self.folder_path]
            self.enableScoreOption()
            self.clearDataDisplay()
            self.ui.listWidget.clear()
            self.ui.listWidget_2.clear()

            for item in self.infoList:
                image_data = self.collection.find_one({"filename": os.path.basename(item.absoluteFilePath())})
                if image_data:
                    self.imageData = [item.absoluteFilePath(), image_data["filename"],
                                      image_data["category"], image_data["noiserate"],
                                      image_data["blur"], image_data["overexposure"],
                                      image_data["dark"], image_data["fluid"]]
                else:
                    self.imageData = [item.absoluteFilePath(), os.path.basename(item.absoluteFilePath()),
                                      None, None, None, None, None]
                self.listImageData.append(self.imageData)

                self.nextImage()
                self.readData()
                self.displayImage()
            self.nextImage()

    def displayImage(self):
        pixmap = QPixmap(self.listImageData[self.currentId][filepath])
        self.ui.display.setPixmap(pixmap.scaled(self.ui.display.size(), Qt.KeepAspectRatio))

    def addImage(self):
        iD = []
        iD2 = []
        self.ui.newItem = QListWidgetItem()
        self.ui.newItem.setSizeHint(QSize(0, 210))
        self.ui.newItem.setData(Qt.UserRole, self.currentId)

        self.ui.thumbnail = QtWidgets.QWidget()
        self.ui.thumbnail.setObjectName("thumbnail")
        self.ui.thumbnailLayout = QtWidgets.QVBoxLayout(self.ui.thumbnail)
        self.ui.thumbnailLayout.setContentsMargins(-1, 5, -1, 5)
        self.ui.thumbnailLayout.setObjectName("thumbnailLayout")
        self.ui.iLabel = QtWidgets.QLabel(self.ui.thumbnail)
        self.ui.iLabel.setText("")
        self.ui.iLabel.setPixmap(QtGui.QPixmap(self.listImageData[self.currentId][filepath]))
        self.ui.iLabel.setScaledContents(True)
        self.ui.iLabel.setObjectName("iLabel")
        self.ui.thumbnailLayout.addWidget(self.ui.iLabel)

        if self.ui.btn_blur.isChecked() or self.ui.btn_over.isChecked() or self.ui.btn_dark.isChecked() or self.ui.btn_fluid.isChecked():
            self.ui.listWidget.addItem(self.ui.newItem)
            self.ui.listWidget.setItemWidget(self.ui.newItem, self.ui.thumbnail)
            for image in range(self.ui.listWidget.count()):
                if self.ui.listWidget.item(image).data(Qt.UserRole) in iD:
                    self.ui.listWidget.takeItem(image)
                else:
                    iD.append(self.ui.listWidget.item(image).data(Qt.UserRole))
            for image in range(self.ui.listWidget_2.count()):
                if self.currentId == self.ui.listWidget_2.item(image).data(Qt.UserRole):
                    self.ui.listWidget_2.takeItem(image)
                    break

        elif self.ui.btn_info.isChecked():
            self.ui.listWidget_2.addItem(self.ui.newItem)
            self.ui.listWidget_2.setItemWidget(self.ui.newItem, self.ui.thumbnail)
            for image in range(self.ui.listWidget_2.count()):
                if self.ui.listWidget_2.item(image).data(Qt.UserRole) in iD2:
                    self.ui.listWidget_2.takeItem(image)
                else:
                    iD2.append(self.ui.listWidget_2.item(image).data(Qt.UserRole))
            for image in range(self.ui.listWidget.count()):
                if self.currentId == self.ui.listWidget.item(image).data(Qt.UserRole):
                    self.ui.listWidget.takeItem(image)
                    break

        elif self.ui.btn_noninfo.isChecked():
            for image in range(self.ui.listWidget.count()):
                if self.currentId == self.ui.listWidget.item(image).data(Qt.UserRole):
                    self.ui.listWidget.takeItem(image)
                    break
            for image in range(self.ui.listWidget_2.count()):
                if self.currentId == self.ui.listWidget_2.item(image).data(Qt.UserRole):
                    self.ui.listWidget_2.takeItem(image)
                    break

    def nextImage(self):
        if self.ui.btn_blur.isChecked() or self.ui.btn_over.isChecked() or self.ui.btn_dark.isChecked() or self.ui.btn_fluid.isChecked() or self.ui.btn_info.isChecked() or self.ui.btn_noninfo.isChecked():
            if self.currentId < self.listLength()-1:
                self.addImage()
                self.cleanData()
                self.writeData()
                self.currentId += 1
                self.clearDataDisplay()
                self.readData()
                self.displayImage()
            else:
                self.addImage()
                self.cleanData()
                self.writeData()
                self.currentId = self.listLength()
                self.clearDataDisplay()
                self.ui.display.clear()
                self.disableScoreOption()

    def backImage(self):
        if self.currentId != 0:
            self.enableScoreOption()
            self.currentId -= 1
            self.clearDataDisplay()
            self.readData()
            self.displayImage()

    def chooseNoiseImage(self):
        self.enableScoreOption()
        self.currentId = self.ui.listWidget.currentItem().data(Qt.UserRole)
        self.clearDataDisplay()
        self.readData()
        self.displayImage()

    def chooseCleanImage(self):
        self.enableScoreOption()
        self.currentId = self.ui.listWidget_2.currentItem().data(Qt.UserRole)
        self.clearDataDisplay()
        self.readData()
        self.displayImage()

    def listLength(self):
        return len(self.listImageData)

    def clearDataDisplay(self):
        self.ui.btn_info.setChecked(False)
        self.ui.btn_noninfo.setChecked(False)
        self.ui.btn_25.setChecked(False)
        self.ui.btn_50.setChecked(False)
        self.ui.btn_75.setChecked(False)
        self.ui.btn_100.setChecked(False)
        self.disableNoiseOption()
        return

    def cleanData(self):
        path = self.listImageData[self.currentId][filepath]
        name = self.listImageData[self.currentId][filename]
        self.listImageData[self.currentId] = [path, name, None, None, None, None, None, None]

    def readData(self):
        data = self.listImageData[self.currentId]
        if data[category] == "None":
            self.disableNoiseOption()
            return
        elif data[category] == "Info":
            self.ui.btn_info.setChecked(True)
            return
        elif data[category] == "Non_Info":
            self.ui.btn_noninfo.setChecked(True)
            return
        elif data[category] == "Noise":
            self.enableNoiseOption()
            if data[noiserate] == 0.25:
                self.ui.btn_25.setChecked(True)
            elif data[noiserate] == 0.50:
                self.ui.btn_50.setChecked(True)
            elif data[noiserate] == 0.75:
                self.ui.btn_75.setChecked(True)
            elif data[noiserate] == 1.00:
                self.ui.btn_100.setChecked(True)

            if data[blur] == 1:
                self.ui.btn_blur.setChecked(True)
            if data[overexposure] == 1:
                self.ui.btn_over.setChecked(True)
            if data[dark] == 1:
                self.ui.btn_dark.setChecked(True)
            if data[fluid] == 1:
                self.ui.btn_fluid.setChecked(True)

    def writeData(self):
        if self.ui.btn_info.isChecked():
            self.listImageData[self.currentId][category] = "Info"
            self.listImageData[self.currentId][noiserate] = "#"
        elif self.ui.btn_noninfo.isChecked():
            self.listImageData[self.currentId][category] = "Non_Info"
            self.listImageData[self.currentId][noiserate] = "#"
        elif self.ui.btn_25.isChecked():
            self.listImageData[self.currentId][category] = "Noise"
            self.listImageData[self.currentId][noiserate] = 0.25
        elif self.ui.btn_50.isChecked():
            self.listImageData[self.currentId][category] = "Noise"
            self.listImageData[self.currentId][noiserate] = 0.50
        elif self.ui.btn_75.isChecked():
            self.listImageData[self.currentId][category] = "Noise"
            self.listImageData[self.currentId][noiserate] = 0.75
        elif self.ui.btn_100.isChecked():
            self.listImageData[self.currentId][category] = "Noise"
            self.listImageData[self.currentId][noiserate] = 1.00
        else:
            self.listImageData[self.currentId][category] = "None"

        if self.ui.btn_blur.isChecked():
            self.listImageData[self.currentId][blur] = 1
        if self.ui.btn_over.isChecked():
            self.listImageData[self.currentId][overexposure] = 1
        if self.ui.btn_dark.isChecked():
            self.listImageData[self.currentId][dark] = 1
        if self.ui.btn_fluid.isChecked():
            self.listImageData[self.currentId][fluid] = 1

        data = {
            "filename": self.listImageData[self.currentId][filename],
            "category": self.listImageData[self.currentId][category],
            "noiserate": self.listImageData[self.currentId][noiserate],
            "blur": self.listImageData[self.currentId][blur],
            "overexposure": self.listImageData[self.currentId][overexposure],
            "dark": self.listImageData[self.currentId][dark],
            "fluid": self.listImageData[self.currentId][fluid]
        }
        self.collection.update_one({"filename": data["filename"]}, {"$set": data}, upsert=True)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    view = MainWindow()

    sys.exit(app.exec_())
