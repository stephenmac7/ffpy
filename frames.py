from getpass import getuser as username
from PySide.QtGui import *
from PySide.QtCore import *

class FileFrame(QFrame):
  """ File Options """
  def __init__(self):
    super(FileFrame, self).__init__()
    self.initUI()

  def initUI(self):
    # Create grid layout
    filegrid = QGridLayout()
    filegrid.setSpacing(10)
    # Create Labels/Selectors
    input_btn = QPushButton("Input File")
    input_btn.clicked.connect(self.getFile)
    output_btn = QPushButton("Output File")
    output_btn.clicked.connect(self.getFile)
    # Create Entries
    self.input_ent = QLineEdit(self)
    self.output_ent = QLineEdit(self)
    # Layout
    filegrid.addWidget(input_btn, 0, 0)
    filegrid.addWidget(output_btn, 1, 0)
    filegrid.addWidget(self.input_ent, 0, 1, 1, 1)
    filegrid.addWidget(self.output_ent, 1, 1, 2, 1)
    self.setLayout(filegrid)

  def getFile(self):
    default_path = "/home/" + username()
    if self.sender().text() == "Input File":
      fname = QFileDialog.getOpenFileName(self, "Input File", default_path)[0]
      self.input_ent.clear()
      self.input_ent.insert(fname)
    elif self.sender().text() == "Output File":
      fname = QFileDialog.getSaveFileName(self, "Output File", default_path)[0]
      self.output_ent.clear()
      self.output_ent.insert(fname)

  @property
  def fileInfo(self):
    return self.input_ent.text(), self.output_ent.text()

class AFrame(QFrame):
  """ Audio Options """
  def __init__(self):
    super(AFrame, self).__init__()
    self.initUI()

  def initUI(self):
    # Create grid layout
    agrid = QGridLayout()
    agrid.setSpacing(10)
    # Create Labels/Boxes For ab and sr
    agrid.addWidget(QLabel("Audio Bitrate", self), 0, 0)
    agrid.addWidget(QLabel("Sample Rate (in Hz)", self), 1, 0)
    self.abr_ent = QLineEdit(self)
    self.asr_ent = QLineEdit(self)
    agrid.addWidget(self.abr_ent, 0, 1)
    agrid.addWidget(self.asr_ent, 1, 1)
    # Create Audio Codec Stuff
    acodecs = ["libvorbis", "libmp3lame", "faac"]
    self.acodec_combo = QComboBox(self)
    for acodec in acodecs:
      self.acodec_combo.addItem(acodec)
    agrid.addWidget(QLabel("Audio Codec", self), 2, 0)
    agrid.addWidget(self.acodec_combo, 2, 1)
    # Set layout
    self.setLayout(agrid)

  @property
  def audioInfo(self):
    return self.abr_ent.text(), self.asr_ent.text(), self.acodec_combo.currentText()
