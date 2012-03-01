import os, sys, shutil
import transmissionrpc, ConfigParser, io
from TVShow import TVShow

cf = ConfigParser.ConfigParser()
cf.readfp(open('ssconfig.cfg'))

#test for MySQL usage
if(cf.has_section('mysqldb'):
  import MySQLdb
  conn=MySQLdb.connect(host=cf.get('mysqldb','host'),user=cf.get('mysqldb','dbuser'),passwd=cf.get('mysqldb','dbpass'),db=cf.get('mysqldb','dbname'))
else:
  conn=false
#creates transmission connection
tc = transmissionrpc.Client(cf.get('trans','host'),port=cf.get('trans','port'),user=cf.get('trans','user'),password=cf.get('trans','pass'))
#gets directory to look in
sDir=cf.get('showscrub','lookin')

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





