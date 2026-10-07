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


#with open("filename.txt", "r") as file:
    #content = file.read()

geometryX = 0
geometryY = 0

content = ""


def write_to_file():
    print("saved")


def minimize_window():
    root.iconify()

def start_drag(event):
    root.x = event.x
    root.y = event.y

def drag_window(event):
    x = root.winfo_x() + event.x - root.x
    y = root.winfo_y() + event.y - root.y
    root.geometry(f"+{x}+{y}")



def start_resize(event):
    root.start_width = root.winfo_width()
    root.start_height = root.winfo_height()
    root.start_x = event.x_root
    root.start_y = event.y_root


def resize_window(event):
    width = root.start_width + (event.x_root - root.start_x)
    height = root.start_height + (event.y_root - root.start_y)

    if width < 200:
        width = 200

    if height < 100:
        height = 100

    root.geometry(f"{width}x{height}")

def maximize_window():
    if root.state() == "zoomed":
        root.state("normal")
    else:
        root.state("zoomed")








def init():
    pass



root = tk.Tk()
root.title("pynotepad")
root.config(bg="#242323")
root.geometry("700x345")
root.update_idletasks()
root.geometry("+%d+%d"%(geometryX, geometryY))
root.overrideredirect(True)


top_bar = tk.Frame(root)
top_bar.pack(side="top", fill="x")
top_bar.config(bg="#333232")

icon_image = tk.PhotoImage(file="./assets/icon.png")

icon = tk.Label(top_bar, image=icon_image, bg="black")
icon.pack(side="left", padx=5)

close_button = tk.Button(top_bar, text="X", command=root.destroy, bg="black", fg="white")
close_button.pack(side="right")


minimize_button = tk.Button(top_bar,text="_",command=minimize_window,bg="black",fg="white")
minimize_button.pack(side="right")

resize_grip = tk.Frame(root, bg="gray", cursor="size_nw_se")
resize_grip.place(relx=1.0, rely=1.0, anchor="se", width=10, height=10)




open_doc_button = tk.Button(top_bar, text="Open File", command=lambda: filedialog.askopenfilename(initialdir="c:/Users/niko/Documents",title="Select a document to edit",filetypes=(("Text files", "*.txt"),)))
open_doc_button.pack(side="left",padx=20)

save_doc_button = tk.Button(top_bar, text="Save File",command=write_to_file)
save_doc_button.pack(side="left",padx=20)


# util for the um winder
top_bar.bind("<Button-1>", start_drag)
top_bar.bind("<B1-Motion>", drag_window)


resize_grip.bind("<Button-1>", start_resize)
resize_grip.bind("<B1-Motion>", resize_window)

maximize_button = tk.Button(top_bar,text="□",command=maximize_window,bg="black",fg="white")
maximize_button.pack(side="right")


main_text_interact = tk.Label(root,text="")


def key_pressed(event):
    global content
    content = event.name
    root.after(0, lambda: main_text_interact.config(text=""))


keyboard.on_press(key_pressed)
root.mainloop()

if __name__ == '__main__':
    pass