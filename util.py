import os
from random import randint

import tkinter as tk
from tkinter import ttk

from tkinter import simpledialog

import subprocess

import urllib.request

import request

from PIL import ImageTk, Image 

import xdb, xfiles
import xattr
import re
import time
import tkinter.font as tkFont
 
from pymediainfo import MediaInfo


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

        self.root.geometry('1200x1080')
        self.root.configure(background="black" )
        self.root.wm_attributes('-alpha', 0.75)

        self.topFrame = tk.Frame(master) #, width=500, height=800)
        self.posterFrame = tk.Frame( self.topFrame ) 

        # self.root.configure(bg="grey")
        self.buttonframe = tk.Frame(self.posterFrame)      

        self.rb = tk.IntVar()
        self.rb.set(1)
        self.r1 = tk.Radiobutton(self.buttonframe,background="black" , text="Movies", variable=self.rb, value=1, command=self.sel)
        self.r1.grid(row=0, column=0)
        self.r2 = tk.Radiobutton(self.buttonframe,background="black" , text="Tv/Series", variable=self.rb, value=2, command=self.sel)
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
        self.entrythingy.grid(row=1, column=4, columnspan = 4)
        self.contents = tk.StringVar() 
        self.contents.set(self.mfiles.path) 
        self.entrythingy["textvariable"] = self.contents 
        self.entrythingy.bind('<Key-Return>', self.print_contents)

        # self.progress = 0.
        # # self.progressVar = tk.DoubleVar()
        # # self.progressVar.set(self.progress)
        # self.progressBar = ttk.Progressbar(self.posterFrame, length=200, mode="determinate") 
        # self.progressBar.grid(row=5, column=0)


        # img = Image.open("./posters/Iron%20Man%20%202008%20.jpg")
        img = Image.open('./posters/test.jpg')
        self.imgs =  (420, 600)
        # imgs =  (300, 420)
        img = img.resize(self.imgs, 0)
        img = ImageTk.PhotoImage(img)
        self.img = img
        self.panel = tk.Label(self.posterFrame, image = self.img, width=self.imgs[0], height=self.imgs[1])
        self.panel.grid(row=1, column=0)
         
        # Add widgets to tab1 
        self.listdata = []
        self.list = tk.Listbox(self.topFrame,   selectbackground='#ff0066', justify="center", font="Herculanum 16", width=60, height=46)   
        # self.list.pack(padx=20,pady=10, expand=True, fill="both")
        self.list.configure(background="black", foreground="white")
 
        self.list.grid(row=0, column=1, padx=8,pady=10)
        self.list.bind('<<ListboxSelect>>', self.onListSelcted)    
        if self.mode == 0:
            a, aa = self.mfiles.showFiles()
            self.setData(a, aa)
        else : self.loadMovers()

        self.font = "American\\ Typewriter 12"
        self.mainText = tk.Text(self.posterFrame,wrap='word',font=self.font, width=40, height=10)
        self.mainText.configure(background="black", foreground="white", highlightbackground="black" )
        self.mainText.grid(row=2, column=0)

        # Insert text into the widget
        self.mainText.insert("1.0", "This is the first line.\n")
        self.mainText.insert("2.0", "This is the second line.")


        self.info = tk.Text(self.posterFrame,wrap='word',font=self.font, width=40, height=4)
        self.info.configure(background="black", foreground="white", highlightbackground="black" )
        self.info.grid(row=3, column=0)
        lib = str(len( xdb.getAllMovieTitles())) + ' movies in library.'
        self.info.insert("1.0", lib + "\n")
        self.info.insert("2.0", "This is the second line.")

        #time
        f = 'Phosphate' + ' 46'
        self.lb = tk.Label(self.posterFrame, width=9, height=1,   font=f) 
        self.lb.configure(background="black", foreground="grey")
        self.lb.grid(row=0, column=0, pady=0, padx=8) 
        self.cb()

        self.posterFrame.configure(background="systemTransparent" )
        self.posterFrame.grid(row=0, column=0)
        self.topFrame.configure(background="systemTransparent" )
        self.topFrame.pack(pady=0, padx=8)

        self.buttonframe.configure(background="black" )
        self.buttonframe.grid(row=4, column=0) #add buttons to the bottom

        self.shiftDown = False
        self.selected = 1
        self.suffixes = ('.mp4', '.avi', '.mkv')
         
        # families = tkFont.families()
        # print(families)

        root.bind("<Button>", self.click_handler)
        root.bind('<KeyPress>', self.onKeyPress) 
        # root.bind("<KeyRelease>", self.onKeyUp)
        self.changeMode()
        self.update() 

  
    def onListSelcted(self, event):
        print('list selected', event)

    def sel(self): 
        print('Raido button clicked', self.rb.get())
        if self.mode == 1:
            self.loadMovers()

    def updateProgress(self, value):
        print('update progress', value)
        # self.progressBar['value'] = value
        # self.root.update_idletasks() # Ensure the GUI updates

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
            self.entrythingy.config(state="normal")


    def addTv(self, r):
        print('adding tv: ', r)
        #check if tv show exisits.
        #if it does not add it. them add the eps
        xdb.addTv(r)

    def addMovie(self, r):
        print('adding movie: ', r)
        xdb.addMovie(r)

    def loadMovers(self):
        if self.rb.get() == 1: 
            m = xdb.getAllMovieTitles()
        else: m = xdb.getAllTvNames()
        # print(m)
        self.setData([], m) 
        self.list.focus_set()
        self.setSelection(1)

    def reload(self, path):
        s, a = self.mfiles.getFiles(path)
        self.setData(s, a)

        

    # def onSelect(self, event):
    #     # Use the event argument if needed
    #     super.onSelect()

    def update(self):
        if self.mode == 0: return

        print('update ui')
        sl = self.get_selected_items()[0]
        # print(sl)
        if self.rb.get() == 2 or 'end of list' in sl: return
        info = xdb.getMovieInfo(sl)
        print('info', info)
        img = Image.open("./posters/"+info[2])
        img = img.resize(self.imgs, 0)
        img = ImageTk.PhotoImage(img)
        self.img = img
        self.panel.config(image=img)
        self.mainText.delete("1.0", "end") 
        self.mainText.delete("2.0", "end") 
        self.mainText.insert("1.0", info[0] + '\n')

        self.citem = info[3] + info[4] 
        fs = os.path.getsize(self.citem)
        # print(fs, 2**30)
        fs /= (2**30)

        dim = str((info[8], info[9]))
        if info[8] == 1920 : dim += ' 1080p'
        elif info[8] == 1280 : dim += ' 720p'
        dim+= ' ' + info[4][-3:] + ' ' 
        dim += f" {fs:.2f} GB"
        self.mainText.insert("2.0", info[6]+ ' ' + dim + '\n')

        duration = info[7]
        print('video meta:', duration, dim)
        vi =   str(int(duration/60//60)) + ' hr +' + str(int(duration/60%60)) + ' mins, '
        vi +=   str(duration//60) + ' mins, ' + str(duration) + ' secs \n'
        self.mainText.insert("3.0", vi+ '\n')
        self.mainText.insert("5.0", info[5]+ '\n')

        #set current item path to use later
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
        if self.mode == 0: #sort files only
            self.listdata.sort(key=str.casefold)  
        l = str(len(self.listdata))
        if self.mode == 0: 
            self.listdata.insert(0,'  ~ ' + l + ' items in directory ~  ')
            self.listdata.append('  ~ ' + l + ' end of list ~  ')
        else:
            e = ' Movers in library ~  '
            if self.rb.get() == 2: e = e.replace('Movers', 'Tv/Series')
            self.listdata.insert(0,'  ~ ' + l + e)
            self.listdata.append('  ~ ' + l + ' end of list ~  ')
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
        width = 0
        height = 0
        if media_info.tracks:
            for track in media_info.tracks:
                print(track)
                if "track_type='Video'" in str(track):
                    print('found video track', track.duration )
                    d = track.duration
                    width = track.width
                    height = track.height
                    print('meta data:' , d, width, height)
                    if d != None:
                        if '.' in str(d): d = str(d).split('.')[0]
                        duration = int(d) // 1000  # Duration in seconds
                        return duration, (width, height)
                elif "track_type='Audio'" in str(track):
                    print('chekcing autio track for duration.')
                    d = track.duration
                    print('meta data:' , d, width, height)
                    if d == None: d = 0
                    if '.' in str(d): d = str(d).split('.')[0]
                    duration = int(d) // 1000  # Duration in seconds
                    return duration, (width, height)
        return None, None

    @staticmethod
    def onSelect(arg):
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
            self.selected = self.get_selected_items()
            item = self.selected[0]
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

    def getDirFiles(self, i, path=None): 
        mi = []
        ri = i.copy()
        #check for directories add items to q
        for f in i:
            print('checking item:',f, path)
            if path==None:
                p  = self.mfiles.path+f
            else: p = path
            print('checking path:',p)
            if not os.path.isfile(p):
                mf, ff = self.mfiles.getFiles(p)
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
                        mdd = [ k if k.endswith(self.suffixes) else None for k in md]
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
            i = self.get_selected_items()
            mi = self.getDirFiles(i) 
            i.extend(mi)


            print('items:', i) 

        else: 
            #custom query one file at a time only!
            i = [self.mfiles.path + q[1]]
            print('query db', i)
        # print(i)
        n = 0
        for m in i: 

            isvid = m.endswith(self.suffixes) 
            if  os.path.isfile(m) and isvid: 
                print(isvid, m)
                print('checking item', m)

                self.progress = 100* n // (len(i))
                n += 1
                # self.progressVar.set(self.progress)
                self.updateProgress(self.progress)
                tv = self.rb.get()==2 
                if q != None:
                    r = request.qdb(q[0], tv)
                else: r = request.qdb(m.split('/')[-1], tv)
                if tv :  
                    print(r) 
                    sn = ''
                    sid = ''
                    for l in r:
                        if 'id' in l: sid = l[4:] 
                        elif 'original_name' in l: sn = l[16:-1] 
                    print('Show: ', sn, sid)
                    txt = i
                    if q !=  None: txt = q[1]
                    x = re.search(r"S(\d+)",txt)
                    y = re.search(r"E(\d+)",txt) 
                    sea = x[0][1:]
                    ep = y[0][1:] 

                    print('season: ' , sea, ' show ep:', ep)
                    sea = int(sea)
                    ep = int(ep)
                    epi = request.tvep(sid, sea, ep)
                    print(epi)
                    return
                rr = request.getInfo(r, '', m)
                print('response check',rr)
                if len(rr) > 0 and rr[0] == '' : 
                    nr.append(rr[4])
                    continue
                if q != None: 
                    print(q[1])
                    rr[4] = q[1]
                pt = rr[4]
                rr[3] = pt[0:pt.rfind('/')+1]
                rr[4] = pt.split('/')[-1] #add the file name in case we used a custom query
                print('path check', rr[3], 'fn:', rr[4])
                path = rr[3] + rr[4] #save the current item path


                print('path  ---:', path)
                duration, dim = self.get_video_metadata(path) #add video info to db
                rr.append(str(duration))
                rr.append(str(dim[0]))
                rr.append(str(dim[1]))
                print(path, duration, dim)
                if self.rb.get() == 1:
                    self.addMovie(rr)
                else: self.addTv(rr)
                request.getPoster(rr[2]) 

        print('no reponse:', len(nr), nr)
        return nr

    def checkDb(self, q = None):
       
        if self.mode == 0: 
            self.addItemsToDb(q)
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

  


    def getQuery(self):
        # self.root.withdraw() 
        v = self.get_selected_items()[0]
        spaces = " " * 24
        p = spaces + "Enter the name and year of the Movie/Series:" + spaces
        i = simpledialog.askstring(title="Test", prompt=p, initialvalue=v)

        print("Running query:", i)
        if len(i) <=1: 
            print('invalid query ', len(i))
            return
        self.checkDb((i, v))

    def setSelection(self, a):

        self.list.selection_clear(0, "end") 
        # a = self.list.get("active")
        self.list.selection_set(a)  
        self.list.selection_anchor(a)
        self.list.activate(a)
        self.list.see(a) 

    def setSelectionJump(self, j):
        si = self.list.curselection()
        c = si[0]
        print('List jump', c, j)
        c += j
        if c <= 0: c = 1
        elif c >= len(self.listdata): c =  len(self.listdata) - 2
        self.setSelection(c)
        jj = c + j
        if jj < len(self.listdata) and jj > 0:
            self.list.see(jj) 
        self.update()

    def onKeyUp(self, event):
        print(event)
        k = event.keycode  
        if k == 943782142 or k == 1010891006:
            print('shift up')
            # self.list.configure(selectmode='BROWSE') 

            self.shiftDown = False

    def shiftJump(self, k):
        print('jump to:', k)
        for i in range(len(self.listdata)):
            if self.listdata[i].startswith(k):
                self.setSelection(i)
                return

    def onKeyPress(self, event):
        print(event)
        k = event.keycode
        if self.shiftDown:
            self.shiftJump(event.keysym)
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
        elif k == 943782142 or k == 1010891006:
            print('shift')
            self.shiftDown = True
        #     self.list.configure(selectmode='MULTIPLE')
        elif k == 2063660802:
            print('arrow Left') 
            self.setSelectionJump(-10)
        elif k == 2080438019:
            print('arrow Right') 
            self.setSelectionJump(10)
        elif k == 201326705:
            #query
            print('q')
            self.getQuery()
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
                ip.append(   self.mfiles.path + self.list.get(i) + ' ')
            print(ip)
            subprocess.call(['open', '-a', 'vlc',  str(ip) ]) 

        elif k == 150995062: 
            print('V')
            if self.mode == 0:
                self.mfiles.openVlc(self.mfiles.path+self.get_selected_items()[0])
            self.mfiles.openVlc(self.citem)

        elif k == 251658354: 
            r = randint(1,self.list.size()-1)
            print('R ', r)   
            #random vid
            # self.list.selection_clear(0) 
            # self.list.selection_set(r) 
            self.setSelection(r)
            self.update()
            # self.click()

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

