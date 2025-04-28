import os
from random import randint

import tkinter as tk
from tkinter import ttk

import subprocess
import request
 



class xfiles:
    def __init__(self,path, ut): 
        super().__init__()
        self.path = path
        self.home = path   
        self.ui = ut

 
    # def click(self):
    #         item = self.get_selected_items()
    #         ip = self.path +item 
    #         print(ip)
    #         if os.path.isfile(ip):
    #           subprocess.call(['open',  ip ]) 
    #         else: 
    #             print('click')
    #             self.setPath()
                
    def setPath(self, items, back=False):
        if(not back):
            self.path += items + '/' #self.get_selected_items() +'/'
        print(self.path)
        d, f = self.getFiles(self.path)
        # self.setOne(d,f) 
        self.ui.setCon(self.path)
        return d, f
 

    def goHome(self):
            self.path = self.home
            self.ui.reload(self.path)
            self.ui.setCon(self.path)

    def button_click(self):
        print("Button clicked!")

    def goUp(self):
            self.path = self.up(self.path)
            self.ui.reload(self.path)
            self.ui.setCon(self.path)

   
    def openDir(self, ip = None):
        if ip == None: 
            ip = self.path 
        print('open dir', ip)
        # if not os.path.isfile(ip):
        subprocess.call(['open', '-R', ip ]) 

    def openVlc(self, i):
        # print(i)
        # ip = self.path  + i[0]
        ip = i
        print('vlc :' ,ip)
        if os.path.isfile(ip):
          subprocess.call(['open', '-a', 'vlc',  ip ]) 
 
     
    def up(self, p):
        print(p)
        l = len(p)
        r = p[0:l-1].rfind('/')
        print(r)
        p = p[0: r+1]
        print(p)
        return p
      

    def getDirFiles(self, i, path=None): 
        mi = []
        ri = i.copy()
        #check for directories add items to q
        for f in i:
            print('checking item:',f, path)
            if path==None:
                p  = self.path+f
            else: p = path
            print('checking path:',p)
            if not os.path.isfile(p):
                mf, ff = self.getFiles(p)
                mi.append((p,mf))
                mi.append((p,ff))
                ri.remove(f) 
                # ri.extend(ff)
                print(mf)
        print(len(mi), mi)
        if len(mi) >0:

            for mm in mi:
                for f in mm[1]:
                    print('  checking item:',f)
                    fp = mm[0]+'/'+f
                    print('  checking item:',fp)
                    md = []
                    if not os.path.isfile(str(fp)):
                        md = self.getDirFiles([f+'/'], fp)
                        print(md)
                        mdd = [ k if k.endswith(self.ui.suffixes) else None for k in md]
                        mz = []
                        for k in mdd:
                            print(k)
                            if k != None:
                                if k is list:
                                    mz.extend(k)
                                else:
                                    mz.append(k)

                        print('zzz', mz)
                        ri.extend(mz) 
                    else:
                        print('adding item:', fp)
                        ri.append(fp) 
        return ri


    def addItemsToDb(self, q):
        #q = (query, filename)
        nr = []
        if q == None:
            i = self.ui.get_selected_items()
            mi = self.getDirFiles(i) 
            i.extend(mi)


            print('items:', i) 

        else: 
            #custom query one file at a time only!
            i = [self.path + q[1]]
            print('query db', i)
        # print(i)
        n = 0
        for m in i: 

            isvid = m.endswith(self.ui.suffixes) 
            if  os.path.isfile(m) and isvid: 
                print(isvid, m)
                print('checking item', m)

                # self.progressVar.set( 100* n // (len(i)) )
                # n += 1
                # self.progressVar.set(self.progress)
                # self.updateProgress()
                tv = self.ui.rb.get()==2 
                if q != None:
                    rr = request.qdb(q[0], tv)
                else: rr = request.qdb(m, tv)
              
                if rr == None:
                    nr.append(m)
                else: 
                    path = m
                    print('path  ---:', m)
                    fs = os.path.getsize(path)
                    # print(fs, 2**30)
                    fs /= (2**30)
                    if self.ui.rb.get() == 1: 

                        duration, dim = self.ui.get_video_metadata(path) #add video info to db
                        rr.append(str(duration))
                        rr.append(str(dim[0]))
                        rr.append(str(dim[1]))
                        rr.append(str(fs))
                        print(path, duration, dim)
                        self.ui.addMovie(rr)
                    else:  

                        duration, dim = self.ui.get_video_metadata(path) #add video info to db
                       

                        print(path, duration, dim, fs)
                        ei = self.ui.request.getTvInfo(rr[1], m)
                        ei[5] = m[0:m.rfind('/')+1]
                        ei[6] = m.split('/')[-1]

                        ei.extend([str(duration), str(dim[0]), str(dim[1]), str(fs)])
                        shows = [ i[0] for i in xdb.getAllTvShows() ]
                        if rr[0] not in shows:
                            print(len(rr))
                            self.ui.xdb.addTv(rr, True)

                        self.ui.addTv(ei)
                        # self.addTvShow()
 
                    request.getPoster(rr[2], tv) 

        print('no reponse:', len(nr), nr)
        return nr

    def getFiles(self, path): 
        files = os.listdir(path)
        print("Files and directories in '", path, "' :")
        # prints all files
        # print(files)

        files = [f for f in files if not (f.count('.srt') or (f[:1]=='.')) ]

        fl = [f for f in files if not os.path.isfile(path+'/'+f)]
        files = [f for f in files if os.path.isfile(path+'/'+f)]

        print(len(fl))
        for f in fl: 
                print(f)
        print()
        for f in files: 
                print(f)
        return fl, files

    def renameFiles(self,path,  c):
        d, ff = self.getFiles(path)
        for f in ff:
            try:
                os.rename(f, f.replace(c, ''))
                print(f"File '{f}' renamed to   successfully.")
            except FileNotFoundError:
                print(f"Error: File '{f}' not found.")
            except FileExistsError:
                 print(f"Error: File   already exists.")
            except Exception as e:
                print(f"An error occurred: {e}")


    def showFiles(self, openDirs = False):
        dr, files = self.getFiles(self.path);
        if(openDirs):
            for d in dr:
                f = self.getFiles(self.path+'/'+d)
                print(f)

        return dr, files

 
if __name__ == '__main__':
    c = os.getcwd()
    x = xfiles(c, None)
    # x.getFiles(c)
    x.renameFiles(c, '[Funxtasy.com] ')


 