
#!/usr/bin/env python3
#!/Users/user/Dev/xmc/bin/activate

#to run
#chmod +x filename 
#./filename

import vlc
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
from copy import deepcopy


class App(tk.Frame):
    def __init__(self):
        self.root = tk.Tk()
        super().__init__(self.root)
        self.pack() 
        self.mode = 0 #0 files 1 db
        self.mfiles = xfiles.xfiles('/Volumes/T7/', self)

        self.root.title("xmc")
      
        self.citem = ''

        self.root.geometry('1000x1080')
        self.root.configure(background="black" )
        self.root.wm_attributes('-alpha', 0.75)

        self.topFrame = tk.Frame(self.root) #, width=500, height=800)
        self.posterFrame = tk.Frame( self.topFrame ) 

        # self.root.configure(bg="grey")
        self.buttonframe = tk.Frame(self.posterFrame)      

        self.rb = tk.IntVar()
        self.rb.set(1)
        self.r1 = tk.Radiobutton(self.buttonframe,background="black" , text="Movies", variable=self.rb, value=1, command=self.sel)
        self.r1.grid(row=0, column=0)
        self.r2 = tk.Radiobutton(self.buttonframe,background="black" , text="Tv/Series", variable=self.rb, value=2, command=self.sel)
        self.r2.grid(row=0, column=1)
        self.r3 = tk.Radiobutton(self.buttonframe,background="black" , text="Collections", variable=self.rb, value=3, command=self.sel)
        self.r3.grid(row=0, column=2)
        self.r3 = tk.Radiobutton(self.buttonframe,background="black" , text="Recent", variable=self.rb, value=4, command=self.sel)
        self.r3.grid(row=0, column=3)

        
        self.modebutton = tk.Button(self.buttonframe,highlightbackground="black" , text="Mode", command=self.changeMode)
        self.modebutton.grid(row=1, column=0)

        self.homebutton = tk.Button(self.buttonframe, highlightbackground="black" ,text="Home", command=self.goHome)
        self.homebutton.grid(row=1, column=1)
  
        self.button = tk.Button(self.buttonframe, highlightbackground="black" ,text=" Up ", command=self.goUp)
        self.button.grid(row=1, column=2)

        self.dbutton = tk.Button(self.buttonframe,highlightbackground="black" , text=" db ", command=self.checkDb)
        self.dbutton.grid(row=1, column=3)

        self.entrythingy = tk.Entry(self.buttonframe, background="black",width=40 )
        self.contents = tk.StringVar() 
        self.contents.set(self.mfiles.path) 
        self.entrythingy["textvariable"] = self.contents 
        self.entrythingy.bind('<Key-Return>', self.print_contents)
        
        self.entrythingy.grid(row=2, column=0, columnspan = 8, pady=1)

        # self.progress = 0.
        # self.progressVar = tk.DoubleVar()
        # self.progressVar.set(0)
        # self.progressBar = ttk.Progressbar(self.posterFrame, variable=self.progressVar, length=200, mode="determinate") 
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
        self.list = tk.Listbox(self.topFrame,   justify="center", font="Herculanum 16", width=46, height=46)   
        # self.list.pack(padx=20,pady=10, expand=True, fill="both")
        self.list.configure( selectbackground='black', selectforeground='#ff0066',background="black", foreground="white")
 
        self.list.grid(row=0, column=1, padx=8,pady=2)
        self.list.bind('<<ListboxSelect>>', self.onListSelcted)    
        if self.mode == 0:
            a, aa = self.mfiles.showFiles()
            self.setData(a, aa)
        else : self.loadMovers()

        self.font = "American\\ Typewriter 12"
        self.mainText = tk.Text(self.posterFrame,wrap='word',font=self.font, width=38, height=6)
        self.mainText.configure(background="black", foreground="white", highlightbackground="black" )
        self.mainText.grid(row=3, column=0)

        # Insert text into the widget
        self.mainText.insert("1.0", "This is the first line.\n")
        self.mainText.insert("2.0", "This is the second line.")


        self.title = tk.Text(self.posterFrame,wrap='word',font=self.font[0:-2]+'24',  width=20, height=1)
        self.title.configure(background="black", foreground="white", highlightbackground="black" )
        self.title.grid(row=2, column=0)
        self.title.tag_configure("center", justify='center')

        self.info = tk.Text(self.posterFrame,wrap='word',font=self.font, width=38, height=4)
        self.info.configure(background="black", foreground="white", highlightbackground="black" )
        self.info.grid(row=4, column=0)
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
        self.topFrame.pack(pady=0, padx=4)

        self.buttonframe.configure(background="black" , width=50)
        self.buttonframe.grid(row=6, column=0, pady=12) #add buttons to the bottom

        self.shiftDown = False
        self.mt = None #text animation
        self.it = None
        self.tt = None
        self.qsave = None
        self.tvShow = None
        self.selected = 1
        self.suffixes = ('.mp4', '.avi', '.mkv')
        self.media = None
         
        # families = tkFont.families()
        # print(families)

        self.root.bind("<Button>", self.click_handler)
        self.root.bind('<KeyPress>', self.onKeyPress) 
        self.root.bind("<KeyRelease>", self.onKeyUp)
        self.changeMode()
        self.update() 

   
    def onListSelcted(self, event):
        print('list selected', event)

    def sel(self): 
        print('Raido button clicked', self.rb.get())
        # if self.mode == 1:
        self.loadMovers()
        self.update()

    def updateProgress(self):

        # print('update progress', self.progressVar.get())
        # self.progressBar['value'] =  self.progressVar.get()
        # self.root.update_idletasks() # Ensure the GUI updates
        pass

    def cb(self, event=None):
        """Display the time every second."""
        # t = time.strftime('%X')

        t = time.strftime("%I:%M:%S")
        self.lb['text'] = t
  
        self.lb.after(1000, self.cb)

    def print_contents(self, event):
        print(self.mode, " Hi. The current entry content is:",
              self.contents.get())
        if self.mode == 0:
            pass
        else:
            self.findItem(self.contents.get())

    def findItem(self, q):
        print('Searching db for: ', q)
        if q == '': 
            # self.listdata = self.qsave
            self.setData([], self.qsave)
            return
        self.qsave = deepcopy(self.listdata)[1:-1]

        d = []
        for i in self.qsave:
            print(i)
            if q in i[0].lower():
                d.append(i)
        self.setData([], d)



        
    def changeMode(self):
        if self.mode == 0: 
            self.mode = 1
            # self.entrythingy.config(state="disabled")
            self.contents.set('')
            self.loadMovers()
        else: 
            self.mode = 0
            self.goHome()
            # self.entrythingy.config(state="normal")
            self.contents.set(self.mfiles.path)


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
        else: m = xdb.getAllTvShows()
        # print(m)
        self.setData([], m) 
        self.list.focus_set()
        self.setSelection(1)

    def showClicked(self):
        s = self.get_selected_items()[0]
        print('Show Clicked:', s)
        self.tvShow = s
        sl = self.list.curselection()[0]
        m = xdb.getAllEps(self.listdata[sl][1])
        m = sorted(m,  key=lambda x: x[3]*100+x[4]) 
        print(m)
        self.setData([], m) 
        self.list.focus_set()
        self.setSelection(1)
        self.update()



    def reload(self, path):
        s, a = self.mfiles.getFiles(path)
        self.setData(s, a)

    def updateText(self, t = None):
        # print('test', t)

        if t != None and self.mt == None: 
            self.mt = [t, 0]
            self.mainText.delete("1.0", "end") 
      
        if self.mt[1] < len(self.mt[0]): 
            self.mainText.insert(tk.END, self.mt[0][self.mt[1]:self.mt[1]+10])
        self.mt[1] += 10
        if self.mt[1] > len(self.mt[0]):
            self.mt[1] = len(self.mt[0])


        if self.mt[1] >= len(self.mt[0]): 
            self.mt = None
        else: self.mainText.after(10, self.updateText)

    def updateTitle(self, t = None):
        # print('test',  t)

        if t != None and self.tt == None: self.tt = [t, 1]
      
        self.title.delete("1.0", "end") 
        self.title.insert("1.0", self.tt[0][0:self.tt[1]]+ '\n')
        self.title.tag_add("center", "1.0", "end")

        self.tt[1] += 1

        if self.tt[1] >= len(self.tt[0]): 
            self.title.delete("1.0", "end") 
            self.title.insert("1.0", self.tt[0]+ '\n')
            self.title.tag_add("center", "1.0", "end")
            self.tt = None
        else: self.title.after(10, self.updateTitle)


    def updateInfo(self, t = None):
        # print('test',  t)

        if t != None and self.it == None: 
            self.it = [t, 0]

            for i in range(len(t)):
                # print(float(i+1), self.it[0][i] )
                self.info.delete(float(i+1), "end") 
      
        i = self.it[1]
        # print(i)   
        if i < len(self.it[0]):
            self.info.insert(float(i+1), str(self.it[0][i]) + ' \n')
        # self.info.tag_add("center", "1.0", "end")

        self.it[1] += 1

        if self.it[1] > len(self.it[0]): 
            self.it = None
        else: self.info.after(120, self.updateInfo)

    # def onSelect(self, event):
    #     # Use the event argument if needed
    #     super.onSelect()

    def update(self):
        if self.mode == 0: return

        print('update ui')
        # self.updateText()
        sl = self.list.curselection()[0]
        # print(sl)
        if 'end of list' in self.listdata[sl][0]: return

        dim = None
        if self.rb.get() == 2:
            print('Tv Mode')
            if self.tvShow == None:
                info = xdb.getTvInfo(self.listdata[sl][1])
                self.citem = None
             
            else: 
                info = xdb.getEpInfo(self.listdata[sl][1])
                print(info)
                self.citem = info[5] + info[6] 

                dim = [(info[10], info[11])]
                self.updateText(info[7])
        elif self.rb.get() == 1:
            info = xdb.getMovieInfo(self.listdata[sl][1])

            self.citem = info[3] + info[4] 
            dim = [(info[8], info[9]) ]
            self.updateText(info[5])
        else: print('Collections')

        print('info', info)

        self.updateTitle(info[0])
        if self.tvShow == None or self.rb.get() == 1:
            pos = './posters/'
            if self.rb.get() == 2:
                pos += 'tv/'
            img = Image.open(pos+info[2])
            img = img.resize(self.imgs, 0)
            img = ImageTk.PhotoImage(img)
            self.img = img
            self.panel.config(image=img)


        if dim != None:
            # fs = os.path.getsize(self.citem)
            # # print(fs, 2**30)
            # fs /= (2**30)

            if dim[0] == 1920 : dim.append(' 1080p')
            elif dim[0] == 1280 :  dim.append(' 720p') 

            dim.append( ' ' + self.citem[-3:] + ' ' ) 
            # dim.append( f" {fs:.2f} GB" )

            duration = info[-6]
            # print('video meta:', duration, dim)
            vi =   str(int(duration/60//60)) + ' hr +' + str(int(duration/60%60)) + ' mins, '
            vi +=   str(duration//60) + ' mins, ' + str(duration) + ' secs ' 

            ds = ' '.join(map(lambda x: str(x), dim))
            i = [ info[6], ds, vi]
            self.updateInfo(i)
 

 

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
            if self.rb.get() == 2: 
                e = e.replace('Movers', 'Tv/Series') 
            self.listdata.insert(0,('  ~ ' + l + e, 0))
            self.listdata.append(('  ~ ' + l + ' end of list ~  ', 0))
        for i in range(len(self.listdata)):
            t = self.listdata[i]
            # t += self.chop(t)
            if self.mode == 1:
                if self.tvShow != None:
                    print(len(t), t[0])
                    tt =  t[0] 
                    if i >= 1 and i < len(self.listdata)-1:
                        tt += ' s'+ str(t[3])+ 'e'+ str(t[4])
                    self.list.insert(i, tt ) 
                else: self.list.insert(i, t[0])  
            else: self.list.insert(i, t)  


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
        print('on select',arg)

    def click_handler(self, event):
        # event also has x & y attributes
        print(str(event.num) + ' x y: ' + str(event.x) + ' ' + str(event.y))
        if event.widget == self.list:
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
            if self.rb.get() == 2 and self.tvShow == None:
                    self.showClicked()
            else:
                self.update()
                ip = self.citem
                print(ip)
                if os.path.isfile(ip):
                  subprocess.call(['open',  ip ]) 
                 

    def goHome(self):
            if self.mode == 0: self.mfiles.goHome()
            else: self.loadMovers()

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

                # self.progressVar.set( 100* n // (len(i)) )
                # n += 1
                # self.progressVar.set(self.progress)
                # self.updateProgress()
                tv = self.rb.get()==2 
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
                    if self.rb.get() == 1: 

                        duration, dim = self.get_video_metadata(path) #add video info to db
                        rr.append(str(duration))
                        rr.append(str(dim[0]))
                        rr.append(str(dim[1]))
                        rr.append(str(fs))
                        print(path, duration, dim)
                        self.addMovie(rr)
                    else:  

                        duration, dim = self.get_video_metadata(path) #add video info to db
                       

                        print(path, duration, dim, fs)
                        ei = request.getTvInfo(rr[1], m)
                        ei[5] = m[0:m.rfind('/')+1]
                        ei[6] = m.split('/')[-1]

                        ei.extend([str(duration), str(dim[0]), str(dim[1]), str(fs)])
                        shows = [ i[0] for i in xdb.getAllTvShows() ]
                        if rr[0] not in shows:
                            print(len(rr))
                            xdb.addTv(rr, True)

                        self.addTv(ei)
                        # self.addTvShow()
 
                    request.getPoster(rr[2], tv) 

        print('no reponse:', len(nr), nr)
        return nr

    def checkDb(self, q = None):
        if self.mode == 0: 
            self.addItemsToDb(q)
        else:
                i = self.get_selected_items()[0]

                if self.rb.get() == 1:
                    xdb.deleteMovie(i)
                    self.loadMovers()
                elif self.rb.get() == 2:
                    sl = self.list.curselection()[0]
                    ep = self.listdata[sl][1]
                    print('check db tv', sl, ep)
                    xdb.deleteEp(ep)
                    self.update()
                    # self.loadMovers()
   
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
        k = event.keycode  
        print('key up!', event, k, type(k))
        if k == 939587838 or k == 1006696702:
            print('shift up')
            # self.list.configure(selectmode='BROWSE') 
            self.shiftDown = False

    def shiftJump(self, k):
        print('jump to:', k)
        for i in range(len(self.listdata)):
            if self.mode == 0:
                if self.listdata[i].startswith(k):
                    print('jumping:', i)
                    self.setSelection(i)
                    return
            else:
                if k.lower() == 't':
                    if self.listdata[i][0].startswith(k) and not self.listdata[i][0].startswith('The'):
                        self.setSelection(i)
                        return

                elif self.listdata[i][0].startswith(k):
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
            if self.mode == 0:
                self.mfiles.goUp()
            elif self.mode == 1:
                if self.rb.get() == 2:
                    self.tvShow = None
                    self.loadMovers()
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
        elif k == 587202672:
            print('P')
            # self.play_pause() 
            self.media.pause()
            
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
                # self.mfiles.openVlc(self.mfiles.path+self.get_selected_items()[0])
              
                ip = self.mfiles.path+self.get_selected_items()[0]
                self.media = vlc.MediaPlayer(ip)
                self.media.play()
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

    def run_osascript(self, script):
        process = subprocess.Popen(['osascript', '-e', script],
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        return stdout.decode('utf-8').strip(), stderr.decode('utf-8').strip()

    def play_pause(self):
        script = 'tell application "Vlc" to playpause'
        stdout, stderr = self.run_osascript(script)
        if stderr:
            print(f"Error: {stderr}")
        else:
            print(stdout)

    # def control_media(self):
    #     script = f'tell application "VLC" to {'pause'}'
    #     subprocess.run(['osascript', '-e', script], capture_output=True)

        # control_media('playpause') # Toggle play/pause
        # control_media('next track') # Skip to next track
        # control_media('previous track') # Go to previous track


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
 

if __name__ == '__main__':
    myapp = App()   
    # start the program
    myapp.mainloop()

