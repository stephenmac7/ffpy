#!/usr/bin/env python3

# A rewrite of ffpy using the pyside toolkit
# Imports
import sys
from PySide.QtGui import *
from PySide.QtCore import *
from ffpy.frames import *
from ffpy.qwidgets import *

class mainApp(QMainWindow):
  def __init__(self, videobool):
    super(mainApp, self).__init__()
    self.video = videobool
    self.initUI()

  def initUI(self):
    # Get Main Widget
    if self.video == True:
      self.mwidget = Video()
      self.setWindowTitle("ffpy Video")
    else:
      self.mwidget = Audio()
      self.setWindowTitle("ffpy Audio")
    self.setCentralWidget(self.mwidget)
    # Create statusbar
    status = self.statusBar()
    status.showMessage("Idle.")
    self.center()
    self.show()

  def center(self):
    """ Center the window. """
    qr = self.frameGeometry()
    cp = QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    self.move(qr.topLeft())

def main():
  app = QApplication(sys.argv)
  ex = AudioVideo()
  app.exec_()
  video = ex.VideoValue
  ex = mainApp(video)
  sys.exit(app.exec_())

if __name__ == '__main__':
  main()
