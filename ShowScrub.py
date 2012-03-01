import os, sys, shutil
import MySQLdb, transmissionrpc
from TVShow import TVShow

conn = MySQLdb.connect (host = "localhost", user = "homeadmin", passwd = "way23ne", db = "homeadmin")
tc = transmissionrpc.Client('localhost', port=9091, user='jeff', password='way23ne')

if(len(sys.argv) == 1):
  sDir = "/mnt/Media/TV/"
else:
  if(sys.argv[1][-1] != "/"):
    sDir = sys.argv[1] + "/"
  else:
    sDir = sys.argv[1]

#checks to see if dir exists
def check_fordir(s,x):
  for dirname in os.listdir(sDir):
    if(dirname == s+" - Season "+x):
      return True
  return False

#checks for same entry, if not adds show
def check_dbshows(a,b,c,d):
   cursor = conn.cursor()
   sql = "SELECT 1 FROM tv_shows WHERE name = '"+a+"' AND season = '"+b+"' AND episode = '"+c+"'"
   cursor.execute(sql)
   row = cursor.fetchone()
   if(row == None):
     sql = "INSERT INTO tv_shows (tv_showsid, name, season, episode, date_dl, date_aired) VALUES (NULL,'"+a+"',"+b+","+c+",'"+d+"',NULL)"
     cursor.execute(sql)
   cursor.close()

#clears completed torrents
for tort in tc.get_files():
  if(tc.get_files()[tort][0]['completed'] == tc.get_files()[tort][0]['size']):
    tc.remove(tort)

#main program
for filename in os.listdir(sDir):
  if(filename[-3:] == "avi"):
    show = TVShow(filename,sDir,os.path.getmtime(sDir + filename))
    if(show.parse_show()):
      if(not check_fordir(show.showname,show.season)):
        os.mkdir(sDir + show.showname +" - Season "+ show.season)
      shutil.move(sDir + filename, sDir + show.showname +" - Season "+ show.season +"/"+ filename)
      check_dbshows(show.showname,show.season,show.episode,show.dldate)
conn.close ()





