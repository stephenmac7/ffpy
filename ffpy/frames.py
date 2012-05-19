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
    filegrid.addWidget(self.input_ent, 0, 1)
    filegrid.addWidget(self.output_ent, 1, 1)
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
    # Create audio codec list
    acodecs = ["libvorbis", "libmp3lame", "libfaac", "wmav2", "copy"]
    # Create the combo box
    self.acodec_combo = QComboBox(self)
    # Add all the codecs in the list.
    for acodec in acodecs:
      self.acodec_combo.addItem(acodec)
    # Label it
    agrid.addWidget(QLabel("Audio Codec", self), 2, 0)
    # Grid it
    agrid.addWidget(self.acodec_combo, 2, 1)
    # Set layout
    self.setLayout(agrid)

  @property
  def audioInfo(self):
    return self.abr_ent.text(), self.asr_ent.text(), self.acodec_combo.currentText()

class VFrame(QFrame):
  """ Video Options """
  def __init__(self):
    super(VFrame, self).__init__()
    self.initUI()

  def initUI(self):
    # Create grid layout
    vgrid = QGridLayout()
    vgrid.setSpacing(10)
    # Create Labels for Video Bitrate, Dimensions, Video Codec, Framerate, crf (x264)
    # In addition, grid them.
    vgrid.addWidget(QLabel("Video Bitrate", self), 0, 0)
    vgrid.addWidget(QLabel("Framerate", self), 1, 0)
    vgrid.addWidget(QLabel("Video Codec", self), 2, 0)
    vgrid.addWidget(QLabel("Dimensions", self), 3, 0)
    vgrid.addWidget(QLabel("x264 CRF", self), 4, 0)
    # Create Entries for Video Br, Dimensions, Framerate, crf
    self.vbr_ent = QLineEdit(self)
    self.vfr_ent = QLineEdit(self)
    self.vdm_ent = QLineEdit(self)
    self.crf_ent = QLineEdit(self)
    # Grid the entries...
    vgrid.addWidget(self.vbr_ent, 0, 1)
    vgrid.addWidget(self.vfr_ent, 1, 1)
    vgrid.addWidget(self.vdm_ent, 3, 1)
    vgrid.addWidget(self.crf_ent, 4, 1)
    # Create a video codec combobox
    # Create video codec list
    vcodecs = ["libtheora", "libvpx", "libx264", "msmpeg4", "mpeg4", "copy"]
    # Create video codec combo box
    self.vcodec_combo = QComboBox(self)
    # Add all the codecs from the list to the combo box
    for vcodec in vcodecs:
      self.vcodec_combo.addItem(vcodec)
    # Grid the vc combo
    vgrid.addWidget(self.vcodec_combo, 2, 1)
    # Set the layout
    self.setLayout(vgrid)

  @property
  def videoInfo(self):
    return self.vbr_ent.text(), self.vfr_ent.text(), self.vdm_ent.text(), self.crf_ent.text(), self.vcodec_combo.currentText()
