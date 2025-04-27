# import re

# #Check if the string starts with "The" and ends with "Spain":

# txt = "Entourage.S01E11 "
# x = re.search(r"S(\d+)",txt)
# y = re.search(r"E(\d+)",txt)
# # xx = re.search(r"S(\d+)E(\d+)",txt)

# if x:
#   print("YES! We have a match!")
#   print(str(x.groups())) 
#   print(str(y.groups())) 
#   # print(x[1])
# else:
#   print("No match")

# import tkinter as tk
# from tkinter import ttk
# from time import sleep


# n = ['fuckit.mp4', 'idk.mkv', 'gg.jpg']
# suffixes = ('.mp4', '.avi', '.mkv')
# for m in n:
#   result = m.endswith(suffixes)
#   print(result)


import json
 
r = '{"name": "John Doe", "age": 30, "city": "New York"}'
data = json.loads(r)
print(data["name"])
print(data.keys())


