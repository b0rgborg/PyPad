import threading
import keyboard
import tkinter as tk
from tkinter import ttk
import markdown
import pyperclip
from tkinter import filedialog
import configparser
from pathlib import Path





config = configparser.ConfigParser()

cfg_file_path = Path("config/vis.ini")
cfg_files = config.read(cfg_file_path)


font_color = config["TEXT"]["font_color"]
bg_color = config["TEXT"]["bg_color"]
top_bar_bg_color = config["TEXT"]["top_bar_bg_color"]
active_bg_top_color = config["TEXT"]["active_bg_top_color"]

### CACHE
cache_file_limit = 10 

Cache_file_path =  Path("cache/cache.ini")
cache_files = config.read(Cache_file_path)


####    



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



root = tk.Tk()
root.title("pynotepad")
root.config(bg=bg_color)
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
top_bar.config(bg=top_bar_bg_color)

icon = tk.Label(top_bar, image=icon_image,bg=top_bar_bg_color)
icon.pack(side="left", padx=5)

close_button = tk.Button(top_bar, image= icon_close, command=root.destroy, bg= top_bar_bg_color, fg="white",activebackground=active_bg_top_color)
close_button.pack(side="right")

maximize_button = tk.Button(top_bar,image= icon_maximize,command=maximize_window,bg=top_bar_bg_color,activebackground=  active_bg_top_color)
maximize_button.pack(side="right")

minimize_button = tk.Button(top_bar,image= icon_minimize,command=minimize_window,bg=top_bar_bg_color,fg="white",activebackground=active_bg_top_color)
minimize_button.pack(side="right")

resize_grip = tk.Frame(root, bg="#333232", cursor="size_nw_se")
resize_grip.place(relx=1.0, rely=1.0, anchor="se", width=20, height=20)


status_label = tk.Label(root,fg=font_color,bg=bg_color)
status_label.pack(side="bottom", anchor="w")

find_text_box = tk.Entry(root,fg=font_color,bg='#258564',)
find_text_box.pack(side= "top",anchor="e")

content_text = tk.Text(root,fg=font_color,height=8,bg= bg_color, undo=True)
content_text.pack(padx=20, pady= 20, expand=True,fill=tk.BOTH)


# functions in list
def open_text_file():
    file_path = filedialog.askopenfilename(title="Select a Text File", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        with open(file_path, 'r') as file:
            content = file.read()
            content_text.delete(1.0, tk.END)  # Clear  content
            content_text.insert(tk.END, content) # add content
            current_dir = file_path


def Save_text_file():
    file_path = filedialog.asksaveasfilename(TEXTextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        try:
            with open(file_path, 'w') as file:
                content = content_text.get("1.0", "end-1c")
                file.write(content)
            status_label.config(text=f"File saved: {file_path}")
        except Exception as e:
            status_label.config(text=f"Error saving file: {str(e)}")


def save_content():
    content = content_text.get("1.0", "end-1c")
    current_dir.write(content)

###################################

# map funcs
file_functions_list = {"Open text file": open_text_file,"Save": save_content,"Save as": Save_text_file}

# Dropdown button
menu_button = tk.Menubutton(top_bar,text="Files",relief="raised",direction="below",bg= bg_color,fg= font_color ,activebackground= active_bg_top_color)

files_menu = tk.Menu(menu_button, tearoff=0)

for i in file_functions_list:
    files_menu.add_command(label=i,command=file_functions_list[i]),menu_button.config(menu=files_menu),menu_button.pack(side="left")

######################################


# functions in list
def undo_content():
    try:
        content_text.edit_undo()
    except tk.TclError:
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


#word 
def find_content():
    pass
"""
    text.tag_remove("found", "1.0", tk.END)
    
    start = "1.0"
    while True:
        # Search for the word
        pos = text.search(word, start, tk.END, nocase=True)
        if not pos:
            break
        
        # Calculate end position based on word length
        end_pos = f"{pos}+{len(word)}c"
        
        # Add highlight tag
        text.tag_add("found", pos, end_pos)
        start = end_pos # Move start to next position

    text.tag_configure("found", background="yellow")

root = tk.Tk()
text = tk.Text(root)
text.pack()
text.insert("1.0", "Python is fun. Python is powerful.")

tk.Button(root, text="Highlight 'Python'", command=lambda: highlight_word("Python")).pack()

"""

def replace_content():
    print("Wednesday selected")

################
# map funcs
edit_functions_list = {"Undo": undo_content,"Redo": redo_content ,"Cut": cut_content,"Copy":copy_content,"Paste":paste_content,"Find":find_content,"Replace":replace_content}

# Dropdown button
menu_button = tk.Menubutton(top_bar,text="Edit",relief="raised",direction="below",fg=font_color , bg= top_bar_bg_color , activebackground= active_bg_top_color)

files_menu = tk.Menu(menu_button, tearoff=0)

for i in edit_functions_list :
    files_menu.add_command(label=i,command=edit_functions_list [i]),menu_button.config(menu=files_menu),menu_button.pack(side="left")


########################


# util for the um winder
top_bar.bind("<Button-1>", start_drag)
top_bar.bind("<B1-Motion>", drag_window)


resize_grip.bind("<Button-1>", start_resize)
resize_grip.bind("<B1-Motion>", resize_window)

content_text.bind("<Control-z>", lambda event: (undo_content(), "break")[1])
content_text.bind("<Control-x>", lambda event: (cut_content(), "break")[1])
content_text.bind("<Control-c>", lambda event: (copy_content(), "break")[1])
content_text.bind("<Control-v>", lambda event: (paste_content(), "break")[1])

root.mainloop()

if __name__ == '__main__':
    pass