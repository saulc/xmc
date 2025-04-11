import os
from random import randint

import tkinter as tk
from tkinter import ttk

import subprocess

import urllib.request

import request

from PIL import ImageTk, Image 

import xdb, xfiles
import xattr

import time
import tkinter.font as tkFont
 
from pymediainfo import MediaInfo


class App(tk.Frame):
    def __init__(self, root,  master):
        super().__init__(master)
        self.pack() 
        self.mode = 1 #0 files 1 db
        self.mfiles = xfiles.xfiles('/Volumes/T7/', self)
        self.root = root
        self.master = master
        self.root.title("xmc")
      
        self.citem = ''

        self.root.geometry('800x1080')
        self.root.configure(background="black" )
        self.root.wm_attributes('-alpha', 0.8)

        self.topFrame = tk.Frame(master, width=500, height=800)
        self.posterFrame = tk.Frame( self.topFrame ) 

        # self.root.configure(bg="grey")
        self.buttonframe = tk.Frame(self.posterFrame)      

        self.rb = 1
        self.r1 = tk.Radiobutton(self.buttonframe,background="black" , text="Movies", variable=self.rb, value=1, command=self.r)
        self.r1.grid(row=0, column=0)
        self.r2 = tk.Radiobutton(self.buttonframe,background="black" , text="Tv/Series", variable=self.rb, value=2, command=self.rr)
        self.r2.grid(row=0, column=1)
        
        self.modebutton = tk.Button(self.buttonframe,highlightbackground="black" , text="Mode", command=self.changeMode)
        self.modebutton.grid(row=1, column=0)

        self.homebutton = tk.Button(self.buttonframe, highlightbackground="black" ,text="Home", command=self.goHome)
        self.homebutton.grid(row=1, column=1)
  
        self.button = tk.Button(self.buttonframe, highlightbackground="black" ,text="Up", command=self.goUp)
        self.button.grid(row=1, column=2)

        self.dbutton = tk.Button(self.buttonframe,highlightbackground="black" , text="db", command=self.checkDb)
        self.dbutton.grid(row=1, column=3)

        self.entrythingy = tk.Entry(self.buttonframe, background="black" )
        self.entrythingy.grid(row=2, column=0, columnspan = 4)
        self.contents = tk.StringVar() 
        self.contents.set(self.mfiles.path) 
        self.entrythingy["textvariable"] = self.contents 
        self.entrythingy.bind('<Key-Return>', self.print_contents)


        # img = Image.open("./posters/Iron%20Man%20%202008%20.jpg")
        img = Image.open('./posters/test.jpg')
        img = img.resize((300, 420), 0)
        img = ImageTk.PhotoImage(img)
        self.img = img
        self.panel = tk.Label(self.posterFrame, image = self.img, width=300, height=420)
        self.panel.grid(row=1, column=0)
         
        # Add widgets to tab1 
        self.listdata = []
        self.list = tk.Listbox(self.topFrame, selectbackground='#ff0066', font="Rockwell 14", width=60, height=42)   
        # self.list.pack(padx=20,pady=10, expand=True, fill="both")
        self.list.configure(background="black", foreground="white")
        self.list.grid(row=0, column=1, padx=8,pady=1)
        self.list.bind('<<ListboxSelect>>', self.onSelect)    
        if self.mode == 0:
            a, aa = self.mfiles.showFiles()
            self.setData(a, aa)
        else : self.loadMovers()

        self.text_widget = tk.Text(self.posterFrame,wrap='word', width=42, height=24)
        self.text_widget.configure(background="black", foreground="white", highlightbackground="black" )
        self.text_widget.grid(row=2, column=0)

        # Insert text into the widget
        self.text_widget.insert("1.0", "This is the first line.\n")
        self.text_widget.insert("2.0", "This is the second line.")


        self.info = tk.Text(self.posterFrame,wrap='word', width=42, height=7)
        self.info.configure(background="black", foreground="white", highlightbackground="black" )
        self.info.grid(row=3, column=0)
        lib = str(len( xdb.getAllMovieTitles())) + ' movies in library.'
        self.info.insert("1.0", lib + "\n")
        self.info.insert("2.0", "This is the second line.")

        #time
        self.lb = tk.Label(self.posterFrame, width=7, height=1,   font='Rockwell 46') 
        self.lb.configure(background="black", foreground="grey")
        self.lb.grid(row=0, column=0) 
        self.cb()

        self.posterFrame.configure(background="systemTransparent" )
        self.posterFrame.grid(row=0, column=0)
        self.topFrame.configure(background="systemTransparent" )
        self.topFrame.pack(pady=23, padx=5)

        self.buttonframe.configure(background="black" )
        self.buttonframe.grid(row=4, column=0) #add buttons to the bottom
 
         
        families = tkFont.families()
        print(families)

        root.bind("<Button>", self.click_handler)
        root.bind('<KeyPress>', self.onKeyPress) 

  
    def r(self): 
        self.rb = 1 
        self.sel()

    def rr(self): 
        self.rb = 2 
        self.sel()

    def sel(self): 
        print('Raido button clicked', self.rb)


    def cb(self, event=None):
        """Display the time every second."""
        # t = time.strftime('%X')

        t = time.strftime("%I:%M:%S")
        self.lb['text'] = t
  
        self.lb.after(1000, self.cb)

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
        self.list.focus_set()
        self.setSelection(1)

    def reload(self, path):
        s, a = self.mfiles.getFiles(path)
        self.setData(s, a)

        
    def onSelect(self, event):
        # Use the event argument if needed
        super.onSelect()

    def update(self):
        if self.mode == 0: return

        print('update ui')
        sl = self.get_selected_items()[0]
        # print(sl)
        info = xdb.getMovieInfo(sl)
        print('info', info)
        img = Image.open("./posters/"+info[2])
        img = img.resize((300, 420), 0)
        img = ImageTk.PhotoImage(img)
        self.img = img
        self.panel.config(image=img)
        self.text_widget.delete("1.0", "end") 
        self.text_widget.delete("2.0", "end") 
        self.text_widget.insert("1.0", info[0] + '\n')
        self.text_widget.insert("2.0", info[6]+ '\n')

        self.citem = info[3] + info[4] #save the current item path
        duration, dim = self.get_video_metadata(self.citem)
        print('wtf', duration, dim)
        vi = str(dim[0]) + 'x' + str(dim[1]) + ' ' + str(duration) + ' secs, ' + str(duration//60) + ' mins \n' + str(int(duration/60//60)) + ' hr +' + str(int(duration/60%60)) + ' mins'
        self.text_widget.insert("3.0", vi+ '\n')
        self.text_widget.insert("5.0", info[5]+ '\n')


        # att = xattr.listxattr(self.citem )  
        # with open(att[1], "r") as file:
        #     content = file.read()
        #     print(content)
        # print(res)

    def setCon(self, s):
        self.contents.set(s)

    def setData(self, s, a):
        self.list.delete(0, self.list.size())
 
        self.listdata = s + a
        self.listdata.sort(key=str.casefold)  
        l = str(len(self.listdata))
        self.listdata.insert(0,l + ' Movers in library')
        self.listdata.append(l + ' end of list')
        for i in range(len(self.listdata)):
            t = self.listdata[i]
            # t += self.chop(t)
            self.list.insert(i, t)  

        if self.list.size() > 0:
            self.list.selection_set(0)



    def get_video_metadata(self, video_path):
        """Retrieves duration and resolution of a video file."""
        media_info = MediaInfo.parse(video_path)
        print('checking meta data', media_info.tracks)
        if media_info.tracks:
            for track in media_info.tracks:
                print(track)
                if "track_type='Video'" in str(track):
                    print('found video track', track.duration )
                    d = track.duration
                    if '.' in str(d): d = str(d).split('.')[0]
                    duration = int(d) // 1000  # Duration in seconds
                    width = track.width
                    height = track.height
                    return duration, (width, height)
        return None, None


    def onSelect(self):
        print('on select')

    def click_handler(self, event):
        # event also has x & y attributes
        print(str(event.num) + ' x y: ' + str(event.x) + ' ' + str(event.y))
        if event.num == 3:
            print("RIGHT CLICK")
            self.click()
        elif event.num == 1:
            print('left click')
            print(event)
            self.update()

    def click(self):
        if self.mode == 0: #files
            item = self.get_selected_items()[0]
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
                print(i)
                for m in i: 
                    r = request.qdb(m, self.rb==2 )
                    rr = self.mfiles.checkDb(r, m)
                    self.addMovie(rr)
                    request.getPoster(rr[2])
            else:
                i = self.get_selected_items()[0]
                xdb.deleteMovie(i)
                self.loadMovers()

   
    def get_selected_items(self):
        selected_indices = self.list.curselection()
        selected_items = [self.list.get(index) for index in selected_indices]
        print(selected_items)
        if len(selected_items) > 0 : return selected_items 
        else: return ''

    '''    
         keysym=Down keycode=2097215233 x=110 y=213>
    <KeyPress event state=Mod3|Mod4 keysym=Up keycode=2113992448 x=110 y=213>
    <KeyPress event state=Mod3|Mod4 keysym=Right keycode=2080438019 x=110 y=213>
    <KeyPress event state=Mod3|Mod4 keysym=Left keycode=2063660802
    '''

    def setSelection(self, a):

        self.list.selection_clear(0, "end") 
        # a = self.list.get("active")
        self.list.selection_set(a)  
        self.list.selection_anchor(a)
        self.list.activate(a)
        self.list.see(a) 


    def onKeyPress(self, event):
        print(event)
        k = event.keycode

        if k == 2113992448:
            print('arrow up', self.list.curselection() )
            if self.list.curselection()[0] <= 0 : 
                print('top of list.') 
                a = len(self.listdata)-2
                self.setSelection(a)
                
            # else:

            #     a = self.list.get("active")
            #     self.setSelection(a)
            print( self.list.curselection())
            self.update()


        elif k == 2097215233:
            print('arrow down') 
            if self.list.curselection()[0] == len(self.listdata)-1 : 
                print('end of list.')  
                self.setSelection(1)
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
            if self.mode == 0: self.mfiles.openDir(self.mfiles.path + self.get_selected_items()[0])
            else:  
                self.mfiles.openDir(self.citem)

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
            if self.mode == 0:
                self.mfiles.openVlc(self.mfiles.path+self.get_selected_items()[0])
            self.mfiles.openVlc(self.citem)

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
# root.config(bg='black')
 

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

