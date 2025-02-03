import os

import tkinter as tk

import subprocess



class App(tk.Frame):
    def __init__(self, master, path):
        super().__init__(master)
        self.pack()
        self.path = path

        self.entrythingy = tk.Entry()
        self.entrythingy.pack(pady = 20)

        # Create the application variable.
        self.contents = tk.StringVar()
        # Set it to some value.
        self.contents.set("this is a variable")
        # Tell the entry widget to watch this variable.
        self.entrythingy["textvariable"] = self.contents

        # Define a callback for when the user hits return.
        # It prints the current value of the variable.
        self.entrythingy.bind('<Key-Return>', self.print_contents)
        # Add widgets to tab1 
        self.one = []
        self.list = tk.Listbox(master) 
        self.list.pack(expand=True, fill="both")
 
        master.bind("<Button>", self.click_handler)

    def print_contents(self, event):
        print("Hi. The current entry content is:",
              self.contents.get())
        

    def setCon(self, s):
        self.contents.set(s)

    def setOne(self, s):
        self.one = s
        for i in range(len(s)):
            self.list.insert(i, s[i])

   

    def click_handler(self, event):
        # event also has x & y attributes
        print(str(event.num) + ' x y: ' + str(event.x) + ' ' + str(event.y))
        if event.num == 3:
            print("RIGHT CLICK")

            item = self.get_selected_items()
            ip = espath(self.path +item ) 
            print(ip)
            subprocess.call(['open',  ip ]) 

    def get_selected_items(self):
        selected_indices = self.list.curselection()
        selected_items = [self.list.get(index) for index in selected_indices]
        print(selected_items)
        return selected_items[0]

def espath(p):
    print(p)
    q = ''
    i = 0
    for l in p:
        # if l.isspace():
        #     q += "\\"
        # i += 1
        # if(i >8):
            q += l
    print(q)
    return q


# Get the list of all files and directories
p = "/Volumes/T7/potter/"
# p = "/Volumes/T7/"
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

    return files

msg = '--- ACME OSX MEDIA CENTER ---'
files = showFiles()
# makeWindow()


root = tk.Tk()
root.config(bg='black')
root.geometry('600x500')
myapp = App(root, p) 
 
myapp.master.title(msg) 
myapp.setOne(files) 

# start the program
myapp.mainloop()