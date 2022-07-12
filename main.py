import os
import shutil
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon, QImage, QFont
from ui import Ui_MainWindow


class ProgrammUI(QtWidgets.QMainWindow):
    def __init__(self):
        super(ProgrammUI, self).__init__()

        # Инициализация приложения
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_UI()
        self.setWindowTitle("File Sorter")
        self.setWindowIcon(QIcon(":/icons/icon.png"))

    def init_UI(self):
        self.ui.lineEdit.setPlaceholderText("Путь до папки")
        self.ui.lineEdit.clearFocus()
        self.ui.progressBar.setValue(0)
        self.ui.pushButton.clicked.connect(self.sortFolder)
        self.ui.progressBar.setMinimumSize(0, 0)
        self.ui.progressBar.setMaximumSize(0, 0)

    def sortFolder(self):
        path = self.ui.lineEdit.text()

        self.ui.progressBar.setMinimumSize(0, 0)
        self.ui.progressBar.setMaximumSize(16777215, 16777215)

        try:
            files = os.listdir(path)
        except Exception as ex:
            self.ui.lineEdit.setText("")
            self.ui.lineEdit.setPlaceholderText(str(ex))
            self.ui.progressBar.setMinimumSize(0, 0)
            self.ui.progressBar.setMaximumSize(0, 0)
            return

        filesCount = len(files)

        for filename in files:
            ext = filename.split('.')[-1]

            fileIndex = files.index(filename)
            progress = 30 * fileIndex / filesCount
            progressPercent = 100 * fileIndex / filesCount
            roundProgress = round(progress)
            exsProgress = 30 - roundProgress

            self.ui.progressBar.setValue(progressPercent)
            # print(f"[{'=' * roundProgress}{'-' * exsProgress}] - {progressPercent}%")

            tempFilename = filename
            clearFilename = tempFilename.replace(ext, '')[0: -1]

            if clearFilename != 'FileSorter':
                if os.path.isdir(f'{path}\\{filename}') and filename != 'folders':
                    try:
                        os.makedirs(f'{path}\\folders', )
                    except FileExistsError:
                        pass

                    try:
                        shutil.move(f'{path}\\{filename}', f'{path}\\folders')
                    except Exception as ex:
                        print(ex)
                else:
                    try:
                        os.makedirs(f'{path}\\{ext}', )
                    except FileExistsError:
                        pass

                    try:
                        shutil.move(f'{path}\\{filename}', f'{path}\\{ext}')
                    except Exception as ex:

                        try:
                            os.rename(f'{path}\\{filename}', f'{path}\\{clearFilename}_1.{ext}')
                            shutil.move(f'{path}\\{filename}', f'{path}\\{ext}')
                        except Exception as ex:
                            print(ex)

        self.ui.progressBar.setValue(100)


app = QtWidgets.QApplication([])
a = ProgrammUI()
a.show()

sys.exit(app.exec())
