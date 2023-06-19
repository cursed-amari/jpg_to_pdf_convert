import fnmatch
import os
import re

from PIL import Image
from loguru import logger

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QFileDialog

from main_window_class import Ui_MainWindow


logger.add("debug.log", format="{time}, {level}, {message}", level="DEBUG", rotation="2 days", retention="2 days")


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.application_func()

    def application_func(self):
        self.setWindowTitle("Img to pdf converter")
        self.progressBar.setValue(0)
        #connections
        self.pushButton_open_folder.clicked.connect(self.path)
        self.pushButton_convert.clicked.connect(self.convert_img)

    @logger.catch
    def path(self, bool_val=False):
        path_to_directory = QFileDialog.getExistingDirectory(self)
        self.hide_progressbar(False)
        if path_to_directory:
            self.file_path_line(path_to_directory)

    @logger.catch
    def file_path_line(self, path):
        self.lineEdit_folder_path.setText(path)
        self.collect_img()

    @logger.catch
    def collect_img(self):
        list_files = os.listdir(self.lineEdit_folder_path.text())
        self.filter_list_file = []

        for entry in list_files:
            if fnmatch.fnmatch(entry, "*.png"):
                self.filter_list_file.append(entry)
        for entry in list_files:
            if fnmatch.fnmatch(entry, "*.jpeg"):
                self.filter_list_file.append(entry)
        for entry in list_files:
            if fnmatch.fnmatch(entry, "*.jpg"):
                self.filter_list_file.append(entry)
        for entry in list_files:
            if fnmatch.fnmatch(entry, "*.bmp"):
                self.filter_list_file.append(entry)

        self.display_img()

    @logger.catch
    def display_img(self):
        self.listWidget_folder_files.clear()
        for i in self.filter_list_file:
            self.listWidget_folder_files.addItem(i)

    @logger.catch
    def convert_img(self, bool_val=False):
        if self.check_out_folder:
            step = 0
            process = 100/len(self.filter_list_file)

            for entry in self.filter_list_file:
                path_to_file = self.lineEdit_folder_path.text() + "/" + entry
                image_1 = Image.open(path_to_file)
                im_1 = image_1.convert('RGB')
                file_name = re.sub(r'\.\w{1,5}$', "", entry)
                im_1.save(f'{os.getcwd()}/pdf/{file_name}.pdf')
                step += process
                self.progressBar.setValue(int(step))

            self.progressBar.setValue(100)
            self.hide_progressbar(True)

    @logger.catch
    def hide_progressbar(self, flag: bool):
        if flag:
            self.progressBar.setValue(0)
            self.progressBar.hide()
            self.label_process.show()
        else:
            self.progressBar.show()
            self.label_process.hide()

    @logger.catch
    def check_out_folder(self):
        if not os.path.exists(os.getcwd() + "\pdf"):
            os.mkdir(os.getcwd() + "\pdf")
        return True


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec())