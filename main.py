import threading
import keyboard
import tkinter as tk
from tkinter import ttk
import markdown
import os
import pyperclip
from tkinter import filedialog

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

geometryX = 0
geometryY = 0

content = ""
current_dir = ""
paste_text = ""

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


icon_image = tk.PhotoImage(file="./assets/icon.png")
icon_close = tk.PhotoImage(file="./assets/close.png")
icon_maximize = tk.PhotoImage(file="./assets/maximize.png")
icon_minimize = tk.PhotoImage(file="./assets/minimize.png")

top_bar = tk.Frame(root)
top_bar.pack(side="top", fill="x")
top_bar.config(bg="#333232")

icon = tk.Label(top_bar, image=icon_image, bg="black")
icon.pack(side="left", padx=5)

close_button = tk.Button(top_bar, image= icon_close, command=root.destroy, bg="#333232", fg="white")
close_button.pack(side="right")

maximize_button = tk.Button(top_bar,image= icon_maximize,command=maximize_window,bg="#333232",fg="white")
maximize_button.pack(side="right")

minimize_button = tk.Button(top_bar,image= icon_minimize,command=minimize_window,bg="#333232",fg="white")
minimize_button.pack(side="right")

resize_grip = tk.Frame(root, bg="#333232", cursor="size_nw_se")
resize_grip.place(relx=1.0, rely=1.0, anchor="se", width=20, height=20)


status_label = tk.Label(root,fg="#E6D9D9",bg="#333232")
status_label.pack(side="bottom", anchor="w")



content_text = tk.Text(root,fg="#EBEBEB",height=8,bg= "#242222")
content_text.pack(padx=20, pady= 20, expand=True,fill=tk.BOTH)


# functions in list
def open_text_file():
    file_path = filedialog.askopenfilename(title="Select a Text File", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'r') as file:
            content = file.read()
            content_text.delete(1.0, tk.END)  # Clear previous content
            content_text.insert(tk.END, content)

def Save_text_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        try:
            with open(file_path, 'w') as file:
                content = content_text.get("1.0", "end-1c")
                file.write(content)
            status_label.config(text=f"File saved: {file_path}")
        except Exception as e:
            status_label.config(text=f"Error saving file: {str(e)}")



def save_content():
    print("Wednesday selected")


# map funcs
file_functions_list = {"Open text file": open_text_file,"Save": save_content,"Save as": Save_text_file}

# Dropdown button
menu_button = tk.Menubutton(top_bar,text="Files",relief="raised",direction="below")

files_menu = tk.Menu(menu_button, tearoff=0)

for i in file_functions_list:
    files_menu.add_command(label=i,command=file_functions_list[i]),menu_button.config(menu=files_menu),menu_button.pack(side="left")

######################################


# functions in list
def undo_content():
    pass

def redo_content():
    print("Tuesday selected")

def cut_content():
    print("Wednesday selected")

def copy_content():
    print("Wednesday selected")


def paste_content():
    paste_text = pyperclip.paste()
    position =content_text.index("insert")
    content_text.insert(position, paste_text)


def find_content():
    print("Wednesday selected")

def replace_content():
    print("Wednesday selected")


# map funcs
edit_functions_list = {"Undo": undo_content,"Redo": redo_content ,"Cut": cut_content,"Copy":copy_content,"Paste":paste_content,"Find":find_content,"Replace":replace_content}

# Dropdown button
menu_button = tk.Menubutton(top_bar,text="Edit",relief="raised",direction="below")

files_menu = tk.Menu(menu_button, tearoff=0)

for i in edit_functions_list :
    files_menu.add_command(label=i,command=edit_functions_list [i]),menu_button.config(menu=files_menu),menu_button.pack(side="left")






##############################################

#open_doc_button = tk.Button(top_bar,bg="#333232", text="Open File", command=lambda: filedialog.askopenfilename(initialdir="c:/Users/niko/Documents",title="Select a document to edit",filetypes=(("Text files", "*.txt"),)))
#open_doc_button.pack(side="left",padx=0)

#save_doc_button = tk.Button(top_bar, text="Save File",command=write_to_file,bg= "#333232")
#save_doc_button.pack(side="left",padx= 0)


# util for the um winder
top_bar.bind("<Button-1>", start_drag)
top_bar.bind("<B1-Motion>", drag_window)


resize_grip.bind("<Button-1>", start_resize)
resize_grip.bind("<B1-Motion>", resize_window)






root.mainloop()

if __name__ == '__main__':
    pass