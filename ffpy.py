#!/usr/bin/env python3

# A rewrite of ffpy using the pyside toolkit
# Imports
import sys
from os.path import splitext
from os import system
from PySide.QtGui import *
from PySide.QtCore import *
from frames import *

# Pick either audio or video
video = False
class AudioVideo(QWidget):
  def __init__(self):
    super(AudioVideo, self).__init__()
    self.initUI()

  def initUI(self):
    self.audio_s = QRadioButton("Audio", self)
    self.video_s = QRadioButton("Video", self)
    next_button = QPushButton("Next", self)
    next_button.clicked.connect(self.closeAndSave)

    hbox = QHBoxLayout()
    hbox.addWidget(self.audio_s)
    hbox.addWidget(self.video_s)
    hbox.addWidget(next_button)
    self.setLayout(hbox)

    self.setWindowTitle("Audio or Video")
    self.center()
    self.show()

  def closeAndSave(self):
    global video
    if self.video_s.isChecked():
      video = True
    QCoreApplication.exit()

  def closeEvent(self, event):
    reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes | 
            QMessageBox.No, QMessageBox.No)
    if reply == QMessageBox.Yes:
      sys.exit("Closed by User.")
    else:
      event.ignore()

  def center(self):
    qr = self.frameGeometry()
    cp = QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    self.move(qr.topLeft())

class Audio(QWidget):
  def __init__(self):
    super(Audio, self).__init__()
    self.initUI()

  def initUI(self):
    # Create Frames
    self.fileframe = FileFrame()
    self.audioframe = AFrame()
    # Create Splitters
    fa_split = QSplitter(Qt.Horizontal)
    fa_split.addWidget(self.fileframe)
    fa_split.addWidget(self.audioframe)
    # Create and connect convert button
    convert_btn = QPushButton("Convert")
    convert_btn.clicked.connect(self.convert)
    # Create layout
    grid = QGridLayout()
    grid.addWidget(fa_split, 0, 0)
    grid.addWidget(convert_btn, 1, 0)
    self.setLayout(grid)

  def convert(self):
    audio_bitrate, audio_samplerate, audio_codec = self.audioframe.audioInfo
    input_file, output_file = self.fileframe.fileInfo
    if input_file:
      if output_file:
        command = "ffmpeg -i " + input_file + " -acodec " + audio_codec
        if audio_bitrate:
          command += " -ab " + audio_bitrate
        if audio_samplerate:
          command += " -ar " + audio_samplerate
        command += " " + output_file
#        system(command)
        xtc = "xterm -e sh -c '" + command + "'"
        system(xtc)
      else:
        msgBox = QMessageBox()
        msgBox.setText("No output file.")
        msgBox.exec_()
    else:
      msgBox = QMessageBox()
      msgBox.setText("No input file.")
      msgBox.exec_()

class mainApp(QMainWindow):
  def __init__(self):
    super(mainApp, self).__init__()
    self.initUI()

  def initUI(self):
    # Get Main Widget
    global video
    if video:
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
    qr = self.frameGeometry()
    cp = QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    self.move(qr.topLeft())

def main():
  app = QApplication(sys.argv)
  ex = AudioVideo()
  app.exec_()
  ex = mainApp()
  sys.exit(app.exec_())

if __name__ == '__main__':
  main()
