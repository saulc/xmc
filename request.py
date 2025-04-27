import requests
import wget
import os
import re
import json

# q = 'fast%20and%20furious%206'
# q = 'finch'

headers = {
"accept": "application/json",
"Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI1MmY5YjIwNGVhYTc1ZDJjNDIwNDI0YTg1NjQxZTg2OCIsIm5iZiI6MTczODU2NTI0Ny4wMTgsInN1YiI6IjY3YTA2NjdmMGQxOWYzMGFjMTk1OGJlOCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.JAPC1o8OdPHWMQfRUishyHT8qO7CvLSqQsCLvE-Ppso"
}

def qdb(dat, tv = False):
    query, y = chop(dat.split('/')[-1], tv)
 
    j = queryMdb(query, y, tv)

    res = j['total_results']
    if res < 1:
        j = queryMdb(query, str(int(y)+1) , tv)
        res = j['total_results']
        if res < 1: return None

    j = j['results'][0] 
    print('results:', len(j), j)
    # print('json test....', j['original_title'],j['poster_path'])

    ds = j['overview'] 
    ds = ds.replace("'", "")
    ds = ds.replace('"', '')
    if tv: 
         rr = [j['original_name'].replace("'", ""), j['id'], j['poster_path'][1:], 1, 1,  ds , j['first_air_date'] ]
    else:
        rr = [j['original_title'].replace("'", ""), j['id'], j['poster_path'][1:], '', dat, ds , j['release_date'] ]

        pt = rr[4]
        rr[3] = pt[0:pt.rfind('/')+1]
        rr[4] = pt.split('/')[-1] #add the file name in case we used a custom query
        print('path check', rr[3], 'fn:', rr[4])

    #get the path/filename
    print(rr)

    return rr

def queryMdb(query, y, tv):
    url = "https://api.themoviedb.org/3/search/movie?query=" + query + "&include_adult=false&language=en-US&page=1"

    if tv : url = url.replace('movie?', 'tv?')
    if len(str(y))>1: url += "&primary_release_year="+str(y)
    print(url)
 
    response = requests.get(url, headers=headers)

    r = response.text
    j = json.loads(r)
    print('keys:', j.keys())
    
    print('json test....', j['results'],j['total_results'])
    return j

def queryEp(id, s, e):
    url = 'https://api.themoviedb.org/3/tv/'+ str(id) + '/season/'+ str(s) + '/episode/'+ str(e) + '?language=en-US'

    print(url)
 
    r = requests.get(url, headers=headers).text
    j = json.loads(r)
    for l in j:
        print(l)

    ds = j['overview']
    ds = ds.replace("'", "")
    ds = ds.replace('"', '')

    rr = [j['name'].replace("'", ""), id, j['id'], s, e, '', '', ds , j['air_date'] ]
    # j.insert()
    return rr


def getInfo(r, path, item):

    # item = self.get_selected_items()
    # # q, y =  self.chop(item) 
    # print(q)
    # r = request.qdb(q, y)
    i = 0
    rl = 0
    dl = 0
    il = 0
    tl = 0
    pl = 0
    for l in r:
        print(i, l)
        if 'id"' in l: il = i
        if 'release_date' in l: rl = i
        if 'original_title' in l: tl = i
        if 'overview' in l: dl = i
        if 'poster_path' in l: pl = i
        i+=1

    ds = r[dl][11:-2] 
    ds = ds.replace("'", "")
    ds = ds.replace('"', '')
    rr = [r[tl][17:-1].replace("'", ""), r[il][4:], r[pl][15:-1], path, item ,ds, r[rl][15:-1] ]  #
    # xdb.addMovie(rr)
    # self.ui.addMovie(rr)
    # xdb.getAllMovies()

    # self.loadMovers()
    return rr

def getTvInfo(id, r):
    print(r) 
    txt = r 
    x = re.search(r"S(\d+)",txt)
    y = re.search(r"E(\d+)",txt) 
    print('tv check', x, y)
    if x == None or y == None: 
        x = re.search(r"s(\d+)",txt)
        y = re.search(r"e(\d+)",txt) 
        if y == None:
            y = re.search(r"e( (\d+))",txt) 
    sea = x[0][1:]
    ep = y[0][1:] 

    print('season: ' , sea, ' show ep:', ep)
    sea = int(sea)
    ep = int(ep)
    epi = queryEp(id, sea, ep)
    print(epi) 
    return epi

def chop( s, tv):
    print(s)
    r = ''
    rr = [] 
    y = 0
    for t in s.split(' '):
        rr += t.split('.')
    print(rr)
    # if len(s) > 1:
    for i in range(len(rr)):
        print(str(i) + ' ' + rr[i])
        try:
            if tv: 
                if len(re.search(r"S(\d+)",rr[i].upper()).groups()):
                    print('found ep thing')
                    break
            if re.search(r"(\d{4})", rr[i]) and (len(rr[i]) == 4 or len(rr[i]) == 6): 
                print('year search', rr[i], rr[i][1:-1])
                if len(rr[i]) > 4:
                    y = rr[i][1:-1]
                else: y = rr[i]
                break
            elif int(rr[i]): 
                if len(rr[i]) == 4 : 
                    y = rr[i]
                    break
            elif rr[i].endswith(['avi', 'mp4', 'mkv']):
                break
            
        except Exception as e:
            print(e)

        if i > 0: r += '%20'
        r +=  rr[i]
        # r += rr[i] # + ' '
    # else: s = s[0]
    r = r.replace('&', '%26')
    print('query' , r)
    return  r, y

def getPoster(poster, tv = False):

    posterurl = 'https://image.tmdb.org/t/p/original/'+poster
    print(posterurl)

    destination_dir = "./posters/"
    if tv: 
        destination_dir += 'tv/'

    os.makedirs(destination_dir, exist_ok=True)
    file_name = os.path.join(destination_dir, poster) #posterurl.split('/')[-1])
    print(file_name)
    # Download the file
    wget.download(posterurl, out=file_name)




if __name__ == '__main__':

	# q = 'iron%20man'
	# qdb(q, 2008)
	q = 'Top%20gear 2002'
	r = qdb(q, True)
	print(r)



