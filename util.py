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

        self.entrythingy = tk.Entry()
        self.entrythingy.pack(pady = 20) 
        self.contents = tk.StringVar() 
        self.contents.set(path) 
        self.entrythingy["textvariable"] = self.contents 
        self.entrythingy.bind('<Key-Return>', self.print_contents)

        # Add widgets to tab1 
        self.one = []
        self.list = tk.Listbox(master, font="Helvetica 11 bold")   
        self.list.pack(expand=True, fill="both")
        self.list.bind('<<ListboxSelect>>', self.onSelect)    
 
        root.bind("<Button>", self.click_handler)
        root.bind('<KeyPress>', self.onKeyPress) 

    def print_contents(self, event):
        print("Hi. The current entry content is:",
              self.contents.get())
        

    def setCon(self, s):
        self.contents.set(s)

    def setOne(self, s):
        self.list.delete(0, self.list.size())
        print(s)
        self.one = s.sort(key=str.casefold)  
        for i in range(len(s)):
            self.list.insert(i, s[i])

        if self.list.size() > 0:
            self.list.selection_set(0)

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
                self.setOne(d+f) 
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
            self.path = up(self.path)
            self.setPath(True)
        elif k == 603979789:
            #enter
            print('select')
            self.click()
        elif k == 889192475:
            #esc
            print('exit')
            self.root.destroy()
        elif k == 67108968: #jk 671088747 637534314
            #esc
            print('home')
            self.path = self.home
            self.setPath(True)

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
myapp1.setOne(dr+files) 
  

 


# start the program
myapp1.mainloop()

