#log
import string
import time

class logger:
  """log information in a file with date/time stamp."""
  version='v0.0.0'
  def __init__(self, log_file_path):
    self.file_path=log_file_path #"setup_GentecPlink.txt"

  #log setup parameter in a file
  def log(self,set):
    current_time = time.localtime()
    strTime=time.strftime('%d/%m/%Y %H:%M:%S', current_time)
    strData=strTime+",\t" +set
    #write to file
    f=open(self.file_path,"a")
    f.write(strData);
    f.write("\n")
    f.close()
