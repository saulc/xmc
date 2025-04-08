import os
from random import randint

import tkinter as tk
from tkinter import ttk

import subprocess

import urllib.request

import request

from PIL import ImageTk, Image 

import xdb



class App(tk.Frame):
    def __init__(self, root,  master, path):
        super().__init__(master)
        self.pack()
        self.path = path
        self.home = path
        self.root = root
        self.master = master
        self.root.title("xmc")

        # self.root.configure(bg="grey")
        self.buttonframe = tk.Frame(master)      
        
        self.homebutton = tk.Button(self.buttonframe, text="Home", command=self.goHome)
        self.homebutton.grid(row=0, column=0)
  
        self.button = tk.Button(self.buttonframe, text="Up", command=self.goUp)
        self.button.grid(row=0, column=1)

        self.dbutton = tk.Button(self.buttonframe, text="db", command=self.checkDb)
        self.dbutton.grid(row=0, column=2)

        self.entrythingy = tk.Entry(self.buttonframe)
        self.entrythingy.grid(row=0, column=3)
        self.contents = tk.StringVar() 
        self.contents.set(path) 
        self.entrythingy["textvariable"] = self.contents 
        self.entrythingy.bind('<Key-Return>', self.print_contents)


        self.topFrame = tk.Frame(master)
        self.posterFrame = tk.Frame( self.topFrame ) 

        img = Image.open("./posters/Iron%20Man%20%202008%20.jpg")
        img = img.resize((300, 420), 0)
        img = ImageTk.PhotoImage(img)
        self.img = img
        self.panel = tk.Label(self.posterFrame, image = self.img, width=300, height=420)
        self.panel.grid(row=0, column=0)
        
        self.xlist = tk.Listbox(self.topFrame, font="Helvetica 14", width=60, height=24)  
        self.xlist.grid(row=0, column=1, padx=2,pady=1)
        self.xlist.bind('<<ListboxSelect>>', self.onSelect)    
        self.loadMovers()

        self.text_widget = tk.Text(self.posterFrame, width=42, height=10)
        self.text_widget.grid(row=1, column=0)

        # Insert text into the widget
        self.text_widget.insert("1.0", "This is the first line.\n")
        self.text_widget.insert("2.0", "This is the second line.")

        self.posterFrame.grid(row=0, column=0)
        self.topFrame.pack(pady=1, padx=1)
      
        # Add widgets to tab1 
        self.one = []
        self.list = tk.Listbox(master, font="Helvetica 14")   
        self.list.pack(padx=20,pady=10, expand=True, fill="both")
        self.list.bind('<<ListboxSelect>>', self.onSelect)    
 

        self.buttonframe.pack(pady=10)  #add buttons to the bottom


        root.bind("<Button>", self.click_handler)
        root.bind('<KeyPress>', self.onKeyPress) 

    def print_contents(self, event):
        print("Hi. The current entry content is:",
              self.contents.get())
        
    def loadMovers(self):
        m = xdb.getAllMovies()
        for i in range( len(m) ):
            self.xlist.insert(i, m[i])  

    def setCon(self, s):
        self.contents.set(s)

    def setOne(self, s, a):
        self.list.delete(0, self.list.size())
 
        self.one = s + a
        self.one.sort(key=str.casefold)  
        for i in range(len(self.one)):
            t = self.one[i]
            # t += self.chop(t)
            self.list.insert(i, t)  

        if self.list.size() > 0:
            self.list.selection_set(0)

    def chop(self, s):
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
                if rr[i][0]=='(': break
                if int(rr[i]): 
                    if len(rr[i]) == 4 : 
                        y = rr[i]
                        break
            except Exception as e:
                print(e)

            if i > 0: r += '%20'
            r +=  rr[i]
            # r += rr[i] # + ' '
        # else: s = s[0]
        print('query' , r)
        return  r, y


    def onSelect(self):
        print('on select')

    def click_handler(self, event):
        # event also has x & y attributes
        print(str(event.num) + ' x y: ' + str(event.x) + ' ' + str(event.y))
        if event.num == 3:
            print("RIGHT CLICK")
            self.click()

    def click(self):
            item = self.get_selected_items()
            ip = self.path +item 
            print(ip)
            if os.path.isfile(ip):
              subprocess.call(['open',  ip ]) 
            else: 
                print('click')
                self.setPath()
                
    def setPath(self, back=False):
                if(not back):
                    self.path += self.get_selected_items() +'/'
                print(self.path)
                d, f = getFiles(self.path)
                self.setOne(d,f) 
                self.setCon(self.path)

    def get_selected_items(self):
        selected_indices = self.list.curselection()
        selected_items = [self.list.get(index) for index in selected_indices]
        print(selected_items)
        if len(selected_items) > 0 : return selected_items[0] 
        else: return ''
    
    def onKeyPress(self, event):
        print(event)
        k = event.keycode
        if k == 855638143:
            #delete
            print('up')
            self.goUp()
        elif k == 603979789 or k == 822083616:
            #enter or space
            print('select')
            self.click()
        elif k == 889192475:
            #esc
            print('exit')
            self.root.destroy()
        elif k == 67108968: 
            print('home')
            self.goHome()
        elif k == 637534314:
            print('J')
            self.openDir()
        elif k == 671088747: 
            print('K')
        elif k == 620757100: 
            print('L')
            
        elif k == 97: 
            print('A')  #play folder
            self.list.selection_clear(0) 
            self.list.selection_set(0, self.list.size())  
            # ip = self.path 
            ip = []
            for i in self.list.curselection():
                ip.append(   self.path + self.list.get(i) + ' ')
            print(ip)
            subprocess.call(['open', '-a', 'vlc',  str(ip) ]) 

        elif k == 150995062: 
            print('V')
            self.openVlc()

        elif k == 251658354: 
            r = randint(0,self.list.size())
            print('R ', r)   
            #random vid
            self.list.selection_clear(0) 
            self.list.selection_set(r) 
            self.click()

    def form(self, s):
        r = ''
        for i in range(0, len(s)):
            l = s[i]
            if l == ' ' or l == '[' or l == '(': 
                r += '\\'
            r += l
        return r 

    def goHome(self):
            self.path = self.home
            self.setPath(True)

    def button_click(self):
        print("Button clicked!")

    def goUp(self):
            self.path = up(self.path)
            self.setPath(True)
   
    def openDir(self):
        ip = self.path 
        print(ip)
        if not os.path.isfile(ip):
          subprocess.call(['open',  ip ]) 

    def openVlc(self):
 
        ip = self.path  + self.get_selected_items()
        print('vlc :' ,ip)
        if os.path.isfile(ip):
          subprocess.call(['open', '-a', 'vlc',  ip ]) 

    def checkDb(self):

        item = self.get_selected_items()
        q, y =  self.chop(item) 
        print(q)
        r = request.qdb(q, y)
        i = 0
        rl = 0
        dl = 0
        tl = 0
        for l in r:
            print(i, l)
            if 'release_date' in l: rl = i
            if 'original_title' in l: tl = i
            if 'overview' in l: dl = i
            i+=1

        ds = r[dl][11:-2] 
        ds = ds.replace("'", "")
        ds = ds.replace('"', '')
        rr = [r[tl][18:-1], self.path, item ,ds, r[rl][16:-1] ]  #
        xdb.addMovie(rr)
        xdb.getAllMovies()


 
def up(p):
    print(p)
    l = len(p)
    r = p[0:l-1].rfind('/')
    print(r)
    p = p[0: r+1]
    print(p)
    return p

# Get the list of all files and directories
# p = "/Volumes/T7/Fast and Furious/"
p = "/Volumes/T7/"
# path = "/Users/user/Dev/xmc"

def getFiles(path):
    path =  path
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

def showFiles(openDirs = False):
    dr, files = getFiles(p);
    if(openDirs):
        for d in dr:
            f = getFiles(p+'/'+d)
            print(f)

    return dr, files


 
imgurl = 'https://image.tmdb.org/t/p/w185/'
msg = '--- ACME OSX MEDIA CENTER ---'
dr, files = showFiles()
# makeWindow()



root = tk.Tk()
root.config(bg='black')
root.geometry('600x1000')
 

# # Create notebook widget
# notebook = ttk.Notebook(root)
# notebook.pack(expand=True, fill="both")

# Create frames for each tab
# tab1 = ttk.Frame(notebook)
# tab2 = ttk.Frame(notebook)
# tab3 = ttk.Frame(notebook)

# notebook.add(tab1, text="Tab 1")
# notebook.add(tab2, text="Tab 2")
# notebook.add(tab3, text="Tab 3")


myapp1 = App(root, root, p)  
myapp1.setOne(dr,files) 
  

 


# start the program
myapp1.mainloop()

