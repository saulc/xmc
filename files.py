import os

import tkinter as tk
from tkinter import ttk

import subprocess



class App(tk.Frame):
    def __init__(self, root,  master, path):
        super().__init__(master)
        self.pack()
        self.path = path
        self.home = path
        self.root = root
        self.master = master
        
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

        self.buttonframe.pack(pady=10)
      
        # Add widgets to tab1 
        self.one = []
        self.list = tk.Listbox(master, font="Helvetica 14")   
        self.list.pack(expand=True, fill="both")
        self.list.bind('<<ListboxSelect>>', self.onSelect)    
 
        root.bind("<Button>", self.click_handler)
        root.bind('<KeyPress>', self.onKeyPress) 

    def print_contents(self, event):
        print("Hi. The current entry content is:",
              self.contents.get())
        

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
        s = s.split('.')
        if len(s) == 1: s = s[0].split(' ')
        print(s)
        # if len(s) > 1:
        for i in range(len(s)):
            try:
                
                if int(s[i]): break
            except Exception as e:
                print(e)
            
                
                r += s[i] # + ' '
        # else: s = s[0]
        print(r)
        return  r


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
        elif k == 67108968: #jk 671088747 637534314
            #esc
            print('home')
            self.goHome()

    def goHome(self):
            self.path = self.home
            self.setPath(True)

    def button_click(self):
        print("Button clicked!")

    def goUp(self):
            self.path = up(self.path)
            self.setPath(True)

    def checkDb(self):

        item = self.get_selected_items()
        q =  self.chop(item) 
        print(q)
        cu = "curl --request GET \\" 
        c1 = "--url 'https://api.themoviedb.org/3/search/movie?query=" + q + "&include_adult=false&language=en-US&page=1'\\" 
        c2 = "--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI1MmY5YjIwNGVhYTc1ZDJjNDIwNDI0YTg1NjQxZTg2OCIsIm5iZiI6MTczODU2NTI0Ny4wMTgsInN1YiI6IjY3YTA2NjdmMGQxOWYzMGFjMTk1OGJlOCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.JAPC1o8OdPHWMQfRUishyHT8qO7CvLSqQsCLvE-Ppso'\\" 
        c3 = "--header 'accept: application/json' "
        cc =  cu + c1 + c2 + c3

        subprocess.call([ cu, c1, c2, c3]) 
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
root.geometry('600x500')
 

# Create notebook widget
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

# Create frames for each tab
tab1 = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)
tab3 = ttk.Frame(notebook)

notebook.add(tab1, text="Tab 1")
notebook.add(tab2, text="Tab 2")
notebook.add(tab3, text="Tab 3")


myapp1 = App(root, tab1, p)  
myapp1.setOne(dr,files) 
  

 


# start the program
myapp1.mainloop()

