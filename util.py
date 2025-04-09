import os
from random import randint

import tkinter as tk
from tkinter import ttk

import subprocess

import urllib.request

import request

from PIL import ImageTk, Image 

import xdb, xfiles



class App(tk.Frame):
    def __init__(self, root,  master):
        super().__init__(master)
        self.pack() 
        self.mode = 0 #0 files 1 db
        self.mfiles = xfiles.xfiles('/Volumes/T7/', self)
        self.root = root
        self.master = master
        self.root.title("xmc")
        self.citem = ''

        # self.root.configure(bg="grey")
        self.buttonframe = tk.Frame(master)      
        
        self.modebutton = tk.Button(self.buttonframe, text="Mode", command=self.changeMode)
        self.modebutton.grid(row=0, column=0)

        self.homebutton = tk.Button(self.buttonframe, text="Home", command=self.goHome)
        self.homebutton.grid(row=0, column=1)
  
        self.button = tk.Button(self.buttonframe, text="Up", command=self.goUp)
        self.button.grid(row=0, column=2)

        self.dbutton = tk.Button(self.buttonframe, text="db", command=self.checkDb)
        self.dbutton.grid(row=0, column=3)

        self.entrythingy = tk.Entry(self.buttonframe)
        self.entrythingy.grid(row=0, column=4)
        self.contents = tk.StringVar() 
        self.contents.set(self.mfiles.path) 
        self.entrythingy["textvariable"] = self.contents 
        self.entrythingy.bind('<Key-Return>', self.print_contents)


        self.topFrame = tk.Frame(master, width=500, height=800)
        self.posterFrame = tk.Frame( self.topFrame ) 

        # img = Image.open("./posters/Iron%20Man%20%202008%20.jpg")
        img = Image.open('./posters/test.jpg')
        img = img.resize((300, 420), 0)
        img = ImageTk.PhotoImage(img)
        self.img = img
        self.panel = tk.Label(self.posterFrame, image = self.img, width=300, height=420)
        self.panel.grid(row=0, column=0)
         
        # Add widgets to tab1 
        self.listdata = []
        self.list = tk.Listbox(self.topFrame, font="Helvetica 14", width=60, height=42)   
        # self.list.pack(padx=20,pady=10, expand=True, fill="both")
        self.list.grid(row=0, column=1, padx=2,pady=1)
        self.list.bind('<<ListboxSelect>>', self.onSelect)    
        if self.mode == 0:
            a, aa = self.mfiles.showFiles()
            self.setData(a, aa)
        else : self.loadMovers()

        self.text_widget = tk.Text(self.posterFrame, width=42, height=24)
        self.text_widget.grid(row=1, column=0)

        # Insert text into the widget
        self.text_widget.insert("1.0", "This is the first line.\n")
        self.text_widget.insert("2.0", "This is the second line.")


        self.info = tk.Text(self.posterFrame, width=42, height=14)
        self.info.grid(row=2, column=0)
        self.info.insert("1.0", "This is the first line.\n")
        self.info.insert("2.0", "This is the second line.")

        self.posterFrame.grid(row=0, column=0)
        self.topFrame.pack(pady=1, padx=1)

        self.buttonframe.pack(pady=10)  #add buttons to the bottom


        root.bind("<Button>", self.click_handler)
        root.bind('<KeyPress>', self.onKeyPress) 

    def print_contents(self, event):
        print("Hi. The current entry content is:",
              self.contents.get())
        
    def changeMode(self):
        if self.mode == 0: 
            self.mode = 1
            self.entrythingy.config(state="disabled")
            self.loadMovers()
        else: 
            self.mode = 0
            self.goHome()
            self.entrythingy.config(state="enabled")


    def addMovie(self, r):
        print('adding movie: ', r)
        xdb.addMovie(r)

    def loadMovers(self):
        m = xdb.getAllMovieTitles()
        print(m)
        self.setData([], m)

    def reload(self, path):
        s, a = self.mfiles.getFiles(path)
        self.setData(s, a)

        
    def update(self):
        if self.mode == 0: return

        print('update ui')
        sl = self.get_selected_items()
        print(sl)
        info = xdb.getMovieInfo(sl)
        print(len(info), info)
        img = Image.open("./posters/"+info[2])
        img = img.resize((300, 420), 0)
        img = ImageTk.PhotoImage(img)
        self.img = img
        self.panel.config(image=img)
        self.text_widget.delete("1.0", "end") 
        self.text_widget.delete("2.0", "end") 
        self.text_widget.insert("1.0", info[0] + '\n')
        self.text_widget.insert("2.0", info[6]+ '\n')
        self.text_widget.insert("3.0", info[5]+ '\n')
        self.citem = info[3] + info[4]

    def setCon(self, s):
        self.contents.set(s)

    def setData(self, s, a):
        self.list.delete(0, self.list.size())
 
        self.listdata = s + a
        self.listdata.sort(key=str.casefold)  
        for i in range(len(self.listdata)):
            t = self.listdata[i]
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
        if self.mode == 0: #files
            item = self.get_selected_items()
            print('items:', item)
            ip = self.mfiles.path + item 
            print(ip)
            if os.path.isfile(ip):
              subprocess.call(['open',  ip ]) 
            else: 
                print('click')
                d, f = self.mfiles.setPath(item, False)
                self.setData(d,f)
        else: #xdb
            self.update()
            ip = self.citem
            print(ip)
            if os.path.isfile(ip):
              subprocess.call(['open',  ip ]) 
                 

    def goHome(self):
            if self.mode == 0: self.mfiles.goHome()
            else: self.loadMovers()

    def button_click(self):
        print("Button clicked!")

    def goUp(self):
            if self.mode == 0: self.mfiles.goUp()
            else: self.up()

    def up(self):
        print('up')

    def checkDb(self):

            if self.mode == 0: 
                i = self.get_selected_items()
                q, y = self.chop(i)
                print(q, y)
                r = request.qdb(q, y)
                self.mfiles.checkDb(r, i)
             

   
    def get_selected_items(self):
        selected_indices = self.list.curselection()
        selected_items = [self.list.get(index) for index in selected_indices]
        print(selected_items)
        if len(selected_items) > 0 : return selected_items[0] 
        else: return ''

    '''    
         keysym=Down keycode=2097215233 x=110 y=213>
    <KeyPress event state=Mod3|Mod4 keysym=Up keycode=2113992448 x=110 y=213>
    <KeyPress event state=Mod3|Mod4 keysym=Right keycode=2080438019 x=110 y=213>
    <KeyPress event state=Mod3|Mod4 keysym=Left keycode=2063660802
    '''

    def onKeyPress(self, event):
        print(event)
        k = event.keycode

        if k == 2113992448:
            print('arrow up')
            self.update()

        elif k == 2097215233:
            print('arrow down')
            self.update()

        elif k == 855638143:
            #delete
            print('up')
            self.mfiles.goUp()
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
            self.mfiles.goHome()
        elif k == 637534314:
            print('J')
            self.mfiles.openDir()
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
            self.mfiles.openVlc()

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
 
    def button_click(self):
        print("Button clicked!")
 

 
imgurl = 'https://image.tmdb.org/t/p/w185/'
msg = '--- ACME OSX MEDIA CENTER ---'
# dr, files = showFiles()
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


myapp1 = App(root, root)   
  

 


# start the program
myapp1.mainloop()

