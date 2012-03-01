import re, time
class TVShow:
  "This class is used to parse a TV show filename and return various pieces of data."

  def __init__(self,fn,dn,dld):
    self.filename = fn
    self.dirloc = dn
    self.__setdldate(dld)
    return

  #set functions
  def __setdldate(self,dld):
    self.dldate = time.strftime("%Y/%m/%d",time.gmtime(dld))
    return

  #parse show name
  def parse_show(self,fn=""):
    if(fn != ""):
      self.filename = fn
    rp = re.compile('S[0-9]{2}E[0-9]{2}')
    rSE = rp.search(self.filename)
    if(rSE == None):
      return
    sSE = rSE.group()
    self.showname = self.filename[:rSE.start() - 1].replace("."," ")
    self.season = sSE[1:3]
    if(self.season[0] == "0") : self.season = self.season[1]
    self.episode = sSE[4:]
    if(self.episode[0] == "0") : self.episode = self.episode[1]
    return True
  
  