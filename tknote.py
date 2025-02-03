import tkinter as tk
from tkinter import ttk

# Create main window
root = tk.Tk()
root.title("Tkinter Notebook Example")

# Create notebook widget
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

# Create frames for each tab
tab1 = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)

# Add tabs to the notebook
notebook.add(tab1, text="Tab 1")
notebook.add(tab2, text="Tab 2")

# Add widgets to tab1
label1 = tk.Label(tab1, text="This is Tab 1")
label1.pack(pady=20)

# Add widgets to tab2
label2 = tk.Label(tab2, text="This is Tab 2")
label2.pack(pady=20)

# Run the main loop
root.mainloop()