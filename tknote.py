# import tkinter as tk
# from tkinter import ttk

# # Create main window
# root = tk.Tk()
# root.title("Tkinter Notebook Example")

# # Create notebook widget
# notebook = ttk.Notebook(root)
# notebook.pack(expand=True, fill="both")

# # Create frames for each tab
# tab1 = ttk.Frame(notebook)
# tab2 = ttk.Frame(notebook)

# # Add tabs to the notebook
# notebook.add(tab1, text="Tab 1")
# notebook.add(tab2, text="Tab 2")

# # Add widgets to tab1
# label1 = tk.Label(tab1, text="This is Tab 1")
# label1.pack(pady=20)

# # Add widgets to tab2
# label2 = tk.Label(tab2, text="This is Tab 2")
# label2.pack(pady=20)

# # Run the main loop
# root.mainloop()


import tkinter as tk
root = tk.Tk()
root.geometry("612x417")
root.title("change label on listbox selection")
root.resizable(0,0)
root.configure(background='lightgrey')


#Show selected currency for from in label
frmcur_text = tk.StringVar()
frmcur = tk.Label(root, textvariable=frmcur_text, font="Helvetica 10 bold", anchor='w', background='lightgrey').place(x=195,y=50)

def onselect(evt):
    # Note here that Tkinter passes an event object to onselect()

    w = evt.widget
    index = int(w.curselection()[0])
    value = w.get(index)
#    print ('You selected item %d: "%s"' % (index, value))
    frmcur_text.set(value)

#Create listboxes for xurrency selection
listbox1 = tk.Listbox(root, font="Helvetica 11 bold", height=3, width=10)
listbox2 = tk.Listbox(root, font="Helvetica 11 bold", height=3, width=10)
listbox1.place(x=300,y=50)
listbox2.place(x=300,y=125)


for i in range(20):
    i = i + 1
    listbox1.insert(1, i)
    listbox2.insert(1, i)


listbox1.bind('<<ListboxSelect>>', onselect)    

cs = listbox1.curselection()

frmcur_text.set(cs)

root.mainloop()