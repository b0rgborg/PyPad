import threading
import keyboard
import tkinter as tk
import markdown
import os
from tkinter import filedialog

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

#with open('filename.txt', 'r', encoding='utf-8') as file:
    #content = file.read()
    #print(content)




geometryX = 0
geometryY = 0


def init():
    pass

root = tk.Tk()
root.title("pynotepad")
root.config(bg="#E4E2E2")
root.geometry("700x345")
root.update_idletasks()

root.geometry("+%d+%d"%(geometryX, geometryY))

#root.filename = filedialog.askopenfilename(initialdir="c:/Users/niko/Documents",title= "select a document to edit ",filetypes = ("txt files","*.txt"))

root.mainloop()

if __name__ == '__main__':
    pass