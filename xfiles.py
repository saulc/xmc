import os
from random import randint

import tkinter as tk
from tkinter import ttk

import subprocess
 



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


 