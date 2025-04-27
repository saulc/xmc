import tkinter as tk
import tkinter.font as tkFont

root = tk.Tk()


root.wm_attributes('-alpha', 0.8)
families = tkFont.families()
print(families)

# Create a font object
c = len(families)//21
for j in range(c):
	for i in range(21):
		n = families[i+j*21]
		myFont = tkFont.Font(family=n, size=12, weight="bold")

		# Use the font in a label
		label = tk.Label(root, text="Hello! " + str(i+j*21) + '  ' + n, font=myFont)
		# label.config(bg='systemTransparent')
		label.grid(row=i, column=j, padx=2,pady=1)
		# label.pack()

root.mainloop()