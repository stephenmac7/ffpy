#!/usr/bin/env python3

# FFMPEG with a Tk GUI

from tkinter import *
import os
from tkinter.filedialog import askopenfilename

class Application(Frame):
  """ A GUI application which controls ffmpeg. """
  def __init__(self, master):
    """ Initialize Frame. """
    super(Application, self).__init__(master)
    self.grid()
    self.create_first_widgets()

  def create_first_widgets(self):
    """ Create design elements. """
    self.type_lbl = Label(self, text = "Type:")
    self.type_lbl.grid(row = 0, column = 0, sticky = W)
    # Create Audio, Video Radio buttons
    self.mediatype = StringVar()
    self.mediatype.set(None)
    types = ["Audio", "Video"]
    # Audio Radio Button
    self.audiorb = Radiobutton(self, text = types[0], variable = self.mediatype, value = types[0])
    self.audiorb.grid(row = 1, column = 0, sticky = W)
    # Video Radio Button
    self.videorb = Radiobutton(self, text = types[1], variable = self.mediatype, value = types[1])
    self.videorb.grid(row = 1, column = 1, sticky = W)
    # Create next button.
    self.next_bttn = Button(self, text = "Next", command = self.delete_widgets)
    self.next_bttn.grid(row = 2, column = 2, sticky = W)
  def delete_widgets(self):
    # Delete Widgets
    self.next_bttn.grid_forget()
    self.videorb.grid_forget()
    self.audiorb.grid_forget()
    self.type_lbl.grid_forget()
    # Initialize Second Page
    self.create_second_widgets()
  def create_second_widgets(self):
    # Create status label
    self.status_lbl = Label(self, text = "Status: Idle/Converting")
    self.status_lbl.grid(row = 0, column = 0, sticky = W)
    # Create input file text box (and label) + selector
    Label(self, text = "Source: ").grid(row = 1, column = 0, sticky = W)
    self.source_file = StringVar()
    self.source_file.set("/path/to/file.con")
    self.source_entry = Entry(self, textvariable=self.source_file)
    self.source_entry.grid(row = 1, column = 1, columnspan = 1, sticky = W)
    Button(self, text = "Select", command = self.fileSelector
           ).grid(row = 1, column = 2, sticky = W)
    Button(self, text = "File Info", command = self.getFileInfo
           ).grid(row = 1, column = 3, sticky = W)
    # Create container dropdown (and label)
    Label(self, text = "Container: ").grid(row = 2, column = 0, sticky = W)
    self.mcontainer = StringVar()
    self.mcontainer.set("webm")
    OptionMenu(self, self.mcontainer, "ogg", "webm", "mp4", "mp3", "aac", "wmv"
               ).grid(row = 2, column = 1, sticky = W)
    # Create acodec optionmenu
    Label(self, text = "Audio Codec: ").grid(row = 3, column = 0, sticky = W)
    self.audioc = StringVar()
    self.audioc.set("Auto")
    OptionMenu(self, self.audioc, "Auto", "libvorbis", "libfaac", "libmp3lame", "flac", "copy"
               ).grid(row = 3, column = 1, sticky = W)
    # Create audio bitrate text box (and label)
    Label(self, text = "Audio Bitrate: ").grid(row = 4, column = 0, sticky = W)
    self.audiob = Entry(self)
    self.audiob.grid(row = 4, column = 1, sticky = W)
    # Everything Video!
    if self.mediatype.get() == "Video":
      # Create dimentions text box (and label)
      Label(self, text = "Dimensions: ").grid(row = 5, column = 0, sticky = W)
      self.dimension_box = Entry(self)
      self.dimension_box.grid(row = 5, column = 1, sticky = W)
      # Create vcodec optionmenu (and label)
      Label(self, text = "Video Codec: ").grid(row = 3, column = 2, sticky = W)
      self.videoc = StringVar()
      self.videoc.set("Auto")
      OptionMenu(self, self.videoc, "Auto", "libvpx", "x264", "libtheora", "copy"
                 ).grid(row = 3, column = 3, sticky = W)
      # Create video bitrate text box (and label)
      Label(self, text = "Video Bitrate: ").grid(row = 4, column = 2, sticky = W)
      self.videob = Entry(self)
      self.videob.grid(row = 4, column = 3, sticky = W)
    # Convert Button
    Button(self, text = "Convert", command = self.convert
           ).grid(row = 6, column = 0, sticky = W)

  def convert(self):
    realsfile = self.source_file.get().replace(" ", "\ ")
    command = "ffmpeg -i " + realsfile + " -y"
    output = os.path.splitext(realsfile)[0] + "." + self.mcontainer.get()
    if self.audiob.get() != "":
      command += " -ab " + self.audiob.get()
    if self.mediatype.get() == "Video":
      if self.videob.get() != "":
        command += " -vb " + self.videob.get()
      if self.dimension_box.get() != "":
        command += " -s " + self.dimension_box.get()
      if self.videoc.get() != "Auto":
        command += " -vcodec " + self.videoc.get()
    if self.audioc.get() != "Auto":
      command += " -acodec " + self.audioc.get()
    command += " " + output
    print("Command: " + command)
    exitstatus = os.system(command)
    if exitstatus == 0:
      self.status_lbl['text'] = "Status: Success!"
    else:
      self.status_lbl['text'] = "Status: Error! " + str(exitstatus)
 
  def fileSelector(self):
    toAdd = askopenfilename()
    self.source_file.set(toAdd)

  def getFileInfo(self):
    if self.source_file.get() != "":
      command = "ffprobe " + self.source_file.get().replace(" ", "\ ")
      os.system(command)

root = Tk()
root.title("ffpy")
app = Application(root)
root.mainloop()
