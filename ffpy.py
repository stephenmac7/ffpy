#!/usr/bin/env python3

# A rewrite of ffpy using the pyside toolkit
# Imports
import sys
from os.path import splitext
from PySide.QtGui import *
from PySide.QtCore import *
from ffpy.frames import *

# Pick either audio or video
video = False
class AudioVideo(QWidget):
  def __init__(self):
    super(AudioVideo, self).__init__()
    self.initUI()

  def initUI(self):
    # Create the widgets
    self.audio_s = QRadioButton("Audio", self)
    self.video_s = QRadioButton("Video", self)
    next_button = QPushButton("Next", self)
    next_button.clicked.connect(self.closeAndSave)
    # Define the layout
    hbox = QHBoxLayout()
    hbox.addWidget(self.audio_s)
    hbox.addWidget(self.video_s)
    hbox.addWidget(next_button)
    self.setLayout(hbox)
    # Do all the extra window stuff
    self.setWindowTitle("Audio or Video")
    self.center()
    self.show()

  def closeAndSave(self):
    # Get the GLOBAL video for usage outside of the class and fuction
    global video
    # Check if the video radio button has been selected, if so make sure the video var. is true.
    if self.video_s.isChecked():
      video = True
    # Exit the application
    QCoreApplication.exit()

  def closeEvent(self, event):
    # If the user attemps to close the application with the exit button make sure they
    # were actually trying to do so. If so shut off everything.
    reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes | 
            QMessageBox.No, QMessageBox.No)
    if reply == QMessageBox.Yes:
      sys.exit("Closed by User.")
    else:
      event.ignore()

  def center(self):
    """ Center the window. """
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
    # Get information from the frames
    audio_bitrate, audio_samplerate, audio_codec = self.audioframe.audioInfo
    input_file, output_file = self.fileframe.fileInfo
    # Make sure the user has specified an input and output file
    if input_file:
      if output_file:
        # Create the command to be run. TODO: Split arguments from command
        command = "ffmpeg -i " + input_file + " -acodec " + audio_codec
        # If the user has specified a bitrate for the audio add that to the command
        if audio_bitrate:
          command += " -ab " + audio_bitrate
        # Same with the sample rate
        if audio_samplerate:
          command += " -ar " + audio_samplerate
        command += " -y " + output_file
        # Create runner
        self.runner = QProcess(self)
        # Make sure newInfo gets all output
        self.runner.readyReadStandardError.connect(self.newErrInfo)
        # Run the command
        self.runner.start(command)
        # Once it's started set message to Converting
        self.parentWidget().statusBar().showMessage("Converting.")
        # If finished, set the status to idle
        self.runner.finished.connect(self.convFinished)
      else:
        msgBox = QMessageBox()
        msgBox.setText("No output file.")
        msgBox.exec_()
        self.parentWidget().statusBar().showMessage("File Error.")
    else:
      msgBox = QMessageBox()
      msgBox.setText("No input file.")
      msgBox.exec_()
      self.parentWidget().statusBar().showMessage("File Error.")

  def convFinished(self, ecode):
    """ After the conversion has finished... """
    # If it's successful...
    if ecode == 0:
      self.parentWidget().statusBar().showMessage("Idle.")
    # If it's not...
    else:
      self.parentWidget().statusBar().showMessage("Conversion Error. Possible: A file had a space in it's name.")

  def newErrInfo(self):
    """ When there's new information coming from ffmpeg do... """
    # Get the new information
    newString = str(self.runner.readAllStandardError())
    # Print the new information for those running the software from the terminal
    print(newString, end=" ")
    # Get the video duration
    if "Duration: " in newString:
      duration = newString.split(": ")[1].split(".")[0]
      durhour, durminute, dursecond = duration.split(":")
      self.durationTotal = int(dursecond) + int(durminute)*60 + int(durhour)*60*60
    # Get the current time
    elif "time=" in newString:
      currentlyAt = newString.split("time=")[1].split(".")[0]
      curhour, curminute, cursecond = currentlyAt.split(":")
      currentTotal = int(cursecond) + int(curminute)*60 + int(curhour)*60*60
      # Calculate the percentage finished.
      finishedPercent = int(round((currentTotal/self.durationTotal)*100, 0))
      # Change the status message to show this.
      self.parentWidget().statusBar().showMessage(str(finishedPercent) + "% Converted.")
      # Also print for those using the terminal to run the command.
      print("\n" + str(finishedPercent) + "% Finished.")

class Video(QWidget):
  def __init__(self):
    super(Video, self).__init__()
    self.initUI()

  def initUI(self):
    # Create Frames
    self.fileframe = FileFrame()
    self.audioframe = AFrame()
    self.videoframe = VFrame()
    # Create splitter between the videoframe and audioframe
    va_split = QSplitter(Qt.Horizontal)
    va_split.addWidget(self.audioframe)
    va_split.addWidget(self.videoframe)
    # Create splitter between vf/af and file frame
    mf_split = QSplitter(Qt.Vertical)
    mf_split.addWidget(self.fileframe)
    mf_split.addWidget(va_split)
    # Create and connect convert button
    convert_btn = QPushButton("Convert")
    convert_btn.clicked.connect(self.convert)
    # Create layout
    grid = QGridLayout()
    grid.addWidget(mf_split, 0, 0)
    grid.addWidget(convert_btn, 1, 0)
    self.setLayout(grid)

  def convert(self):
    # Get information from the audio frame
    audio_bitrate, audio_samplerate, audio_codec = self.audioframe.audioInfo
    # Get information from the file frame
    input_file, output_file = self.fileframe.fileInfo
    # Get information from the video frame
    video_bitrate, video_framerate, video_dimensions, video_crf, video_codec = self.videoframe.videoInfo
    # Make sure the user has specified an input and output file
    if input_file:
      if output_file:
        # Create the command to be run. TODO: Split arguments from command
        command = "ffmpeg -i " + input_file + " -acodec " + audio_codec
        # Audio stuff
        ## If the user has specified a bitrate for the audio add that to the command
        if audio_bitrate:
          command += " -ab " + audio_bitrate
        ## Same with the sample rate
        if audio_samplerate:
          command += " -ar " + audio_samplerate
        # Video Stuff
        ## Add the video codec
        command += " -vcodec " + video_codec
        ## If the user has specified a bitrate for the video add that to the command
        if video_bitrate:
          command += " -vb " + video_bitrate
        ## If the user has specified a framerate add that to the command
        if video_framerate:
          command += " -r " + video_framerate
        ## If the user has specified certain output dimensions add that to the command
        if video_dimensions:
          command += " -s " + video_dimensions
        ## If the codec is libx264 and the user has specified a crf, add that to the command
        if video_crf:
          if video_codec == "libx264":
            command += " -crf " + video_crf
        command += " -y " + output_file
        # Create runner
        self.runner = QProcess(self)
        # Make sure newInfo gets all output
        self.runner.readyReadStandardError.connect(self.newErrInfo)
        # Run the command
        self.runner.start(command)
        # Once it's started set message to Converting
        self.parentWidget().statusBar().showMessage("Converting.")
        # If finished, set the status to idle
        self.runner.finished.connect(self.convFinished)
      else:
        msgBox = QMessageBox()
        msgBox.setText("No output file.")
        msgBox.exec_()
        self.parentWidget().statusBar().showMessage("File Error.")
    else:
      msgBox = QMessageBox()
      msgBox.setText("No input file.")
      msgBox.exec_()
      self.parentWidget().statusBar().showMessage("File Error.")

  def convFinished(self, ecode):
    """ After the conversion has finished... """
    # If it's successful...
    if ecode == 0:
      self.parentWidget().statusBar().showMessage("Idle.")
    # If it's not...
    else:
      self.parentWidget().statusBar().showMessage("Conversion Error. Possible: A file had a space in it's name.")

  def newErrInfo(self):
    """ When there's new information coming from ffmpeg do... """
    # Get the new information
    newString = str(self.runner.readAllStandardError())
    # Print the new information for those running the software from the terminal
    print(newString, end=" ")
    # Get the video duration
    if "Duration: " in newString:
      duration = newString.split(": ")[1].split(".")[0]
      durhour, durminute, dursecond = duration.split(":")
      self.durationTotal = int(dursecond) + int(durminute)*60 + int(durhour)*60*60
    # Get the current time
    elif "time=" in newString:
      currentlyAt = newString.split("time=")[1].split(".")[0]
      curhour, curminute, cursecond = currentlyAt.split(":")
      currentTotal = int(cursecond) + int(curminute)*60 + int(curhour)*60*60
      # Calculate the percentage finished.
      finishedPercent = int(round((currentTotal/self.durationTotal)*100, 0))
      # Change the status message to show this.
      self.parentWidget().statusBar().showMessage(str(finishedPercent) + "% Converted.")
      # Also print for those using the terminal to run the command.
      print("\n" + str(finishedPercent) + "% Finished.")

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
    """ Center the window. """
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
