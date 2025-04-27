import sqlite3
import datetime


def xdb(command, wherearg=None ):
    con = sqlite3.connect('xmc.db') 
    cur = con.cursor()
    r = []
    m = 0
    # print('xdb: ', command)
    if wherearg == None: 
        m = cur.execute(command)
    else: m = cur.execute(command, (wherearg,))

    for row in m:
            # print(row)
            r.append(row)
    # print(r)
    con.commit()
    con.close()

    return r



def addMovie(info):
 
    today = datetime.date.today()
    t = today.strftime("%Y-%m-%d")
    print(today, t)
    v = "INSERT INTO movies VALUES " + "('"  
    for i in info:
        v+= str(i) + "','"
    v += t+"', 0 )"

    xdb(v)

def getMovieInfo(t):  
    r = []
    c = 'SELECT * FROM movies  WHERE  id =?'
    r = xdb(c, t) 
 
    if len(r) > 0:
        r = r[0]
    # print('zdb', r)
    return r  


def setMovieTitle(t, nv):  

    con = sqlite3.connect('xmc.db') 
    cur = con.cursor()
    cur.execute("UPDATE movies SET title = ? WHERE title = ? ", (nv, t))
    con.commit()
    con.close()

def getAllMovieTitles(): 
    r = []
    c = "SELECT title, id FROM movies ORDER BY  (CASE WHEN title LIKE 'The %' THEN substr(title,5)  ELSE title END)"
    r = xdb(c) 
    # r = [i[0] for i in r]
    return r 

def getAllMovies(): 
    r = []
    c = 'SELECT * FROM movies ORDER BY title'
    r = xdb(c)
    return r

def deleteMovie(t): 
    c = 'DELETE FROM movies WHERE  title =?'
    xdb(c, t)
 

def createMovieTable():
    # Create table
    print('Create Movie Table')
    c = '''CREATE TABLE movies (title text, id integer, poster text, fpath text, fname text, description text, releasedate date,  duration integer, width integer, height integer, filesize real, dateadded date, plays integer)'''
    xdb(c)
#---------------------- tv ----------------------

def addTv(info, show=False):
 
    today = datetime.date.today()
    t = today.strftime("%Y-%m-%d")
    print(today, t)
    if show: 
        v = "INSERT INTO tv VALUES " + "('"  
    else: v = "INSERT INTO ep VALUES " + "('"  
    for i in info:
        v+= str(i) + "','"
    if show: v += t+"')"
    else: v += t+"', 0 )"

    xdb(v)

def getAllTvShows(): 
    r = []
    c = 'SELECT showname, id FROM tv ORDER BY showname'
    r = xdb(c) 
    # r = [i[0] for i in r]
    return r 

def getAllEpNames(): 
    r = []
    c = 'SELECT title, eid, id FROM ep ORDER BY title'
    r = xdb(c) 
    # r = [i[0] for i in r]
    return r 

def getAllEps(sid): 
    r = []
    c = 'SELECT title, eid, id, season, episode FROM ep WHERE  id =?'
    r = xdb(c, sid) 
    # r = [i[0] for i in r]
    return r 


def getTvInfo(t):  
    r = []
    c = 'SELECT * FROM tv  WHERE  id =?'
    r = xdb(c, t) 
 
    if len(r) > 0:
        r = r[0]
    # print('zdb', r)
    return r  

def getEpInfo(t):  
    r = []
    c = 'SELECT * FROM ep  WHERE  eid =?'
    r = xdb(c, t) 
 
    if len(r) > 0:
        r = r[0]
    # print('zdb', r)
    return r  


def deleteEp(t): 
    c = 'DELETE FROM ep WHERE  eid =?'
    xdb(c, t)
 

def createTvTable():
    # Create table
    print('Create Tv Table')
    c = '''CREATE TABLE tv (showname text, id integer, poster text,  seasons integer, episodes integer,  description text, releasedate date, dateadded date)'''
    xdb(c)

def createEpTable():
    # Create table
    print('Create Ep Table')
    c = '''CREATE TABLE ep (title text, id integer,  eid integer, season integer,  episode integer, fpath text, fname text, description text, releasedate date, duration integer, width integer, height integer, filesize real,  dateadded date,  plays integer)'''
    xdb(c)

def deleteTvTable():
    # Delete table
    print('Delete Tv Table')
    c = '''DROP TABLE tv '''
    xdb(c)

def deleteEpTable():
    # delete ep table
    print('Delete Ep Table')
    c = '''DROP TABLE ep '''
    xdb(c)

def deleteMovieTable():
    # delete table
    print('Delete Movie Table')
    c = '''DROP TABLE movies '''
    xdb(c)

def getTime():
 
    today = datetime.date.today()
    t = today.strftime("%Y-%m-%d")
    print(t)


if __name__ == '__main__':
    # deleteTvTable()
    # deleteEpTable()
    # createTvTable()
    # createEpTable()

    deleteMovieTable()
    createMovieTable()
    # r = 'Return of the Jedi'
    # r = 'The Empire Strikes Back'
    # r = '功夫瑜伽'
    # setMovieTitle(r, 'Kung Fu Yoga')
    getTime()