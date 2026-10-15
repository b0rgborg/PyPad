import tkinter as tk
from tkinter import ttk
import pyperclip
from tkinter import filedialog
import configparser
from pathlib import Path


config = configparser.ConfigParser()

cfg_file_path = Path("config/cfg.ini")
cfg_files = config.read(cfg_file_path)


font_color = config["TEXT"]["font_color"]
bg_color = config["TEXT"]["bg_color"]
top_bar_bg_color = config["TEXT"]["top_bar_bg_color"]
active_bg_top_color = config["TEXT"]["active_bg_top_color"]

###
always_on_top_bool = config["SETTINGS"]["always_on_top"]



###


### CACHE
cache_file_limit = 10 

cache_file_path = Path("cache/cache.txt")

def write_to_cache(directory: str):
    with open(cache_file_path, "a", encoding="utf-8") as file:
        file.write(directory +"\n")

def clear_cache():
    with open(cache_file_path, "w", encoding="utf-8") as file:
        file.truncate(0)

def count_dirs_in_cache():
    with open(cache_file_path, "r", encoding="utf-8") as file:
        return sum(1 for i in file)

def check_cache_recent_text():
    with open(cache_file_path, "r", encoding="utf-8") as file:
        current_dir = file.readline()
        if current_dir:
            with open(current_dir, 'r') as file:
                content = file.read()
                content_text.delete(1.0, tk.END)  # Clear  content
                content_text.insert(tk.END, content) # add content

#with open("example.txt", "w", encoding="utf-8") as file:
    #cache_string = cache_file_path.readlines()


####    

geometryX = 0
geometryY = 0


content = ""
current_dir = ""

paste_text = ""


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

close_button = tk.Button(top_bar, image= icon_close, command=root.destroy, bg= top_bar_bg_color, fg=font_color,activebackground=active_bg_top_color)
close_button.pack(side="right")

maximize_button = tk.Button(top_bar,image= icon_maximize,command=maximize_window,bg=top_bar_bg_color,activebackground=  active_bg_top_color)
maximize_button.pack(side="right")

minimize_button = tk.Button(top_bar,image= icon_minimize,command=minimize_window,bg=top_bar_bg_color,fg=font_color,activebackground=active_bg_top_color)
minimize_button.pack(side="right")

resize_grip = tk.Frame(root, bg="#333232", cursor="size_nw_se")
resize_grip.place(relx=1.0, rely=1.0, anchor="se", width=20, height=20)


status_label = tk.Label(root,fg=font_color,bg=bg_color)
status_label.pack(side="bottom", anchor="w")

find_text_box = tk.Entry(root,fg=font_color,bg='#258564',)
find_text_box.pack(side= "top",anchor="e")
find_text_box.destroy()

content_text = tk.Text(root,fg=font_color,height=8,bg= bg_color, undo=True)
content_text.pack(padx=20, pady= 20, expand=True,fill=tk.BOTH)





# functions in list
def open_text_file():
    global current_dir
    file_path = filedialog.askopenfilename(title="Select a Text File", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        with open(file_path, 'r') as file:
            content = file.read()
            content_text.delete(1.0, tk.END)  # Clear  content
            content_text.insert(tk.END, content) # add content
            current_dir = file_path
            #write_to_cache(current_dir)
            status_label.config(text=f"File Opened: {file_path}")


def Save_text_file():
    file_path = filedialog.asksaveasfilename(title="Save File",defaultextension=".txt",filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        try:
            with open(file_path, 'w',encoding="utf-8") as file:
                content = content_text.get("1.0", "end-1c")
                file.write(content)
                status_label.config(text=f"File saved: {file_path}")
        except Exception as e:
            status_label.config(text=f"Error saving file: {str(e)}")


def save_content():
    global current_dir
    content = content_text.get("1.0", "end-1c")

    if not current_dir:
        Save_text_file()
        return
    with open(current_dir, "w", encoding="utf-8") as file:
        file.write(content)

###################################

# map funcs
file_functions_list = {"Open text file": open_text_file,"Save": save_content,"Save as":Save_text_file}

# Dropdown button
file_menu_button = tk.Menubutton(top_bar,text="Files",relief="raised",direction="below",bg= bg_color ,fg= font_color,activebackground= active_bg_top_color)

files_menu = tk.Menu(file_menu_button, tearoff=0,bg= bg_color ,fg= font_color,activebackground= active_bg_top_color )

for i in file_functions_list:
    files_menu.add_command(label=i,command=file_functions_list[i]),file_menu_button.config(menu=files_menu),file_menu_button.pack(side="left")


######################################


# functions in list
def undo_content():
    try:
        content_text.edit_undo()
    except tk.TclError:
        pass

def redo_content():
    try:
        content_text.edit_redo()
    except tk.TclError:
            pass

def cut_content():
    try:
        selected_text = content_text.get(tk.SEL_FIRST, tk.SEL_LAST)
        pyperclip.copy(selected_text)
        content_text.delete(tk.SEL_FIRST, tk.SEL_LAST)
    except tk.TclError:
        pass


def copy_content():
    try:
        selected_text = content_text.get(tk.SEL_FIRST, tk.SEL_LAST)
        pyperclip.copy(selected_text)
    except tk.TclError:
        pass

def paste_content():
    paste_text = pyperclip.paste()
    position =content_text.index("insert")
    content_text.insert(position, paste_text)


#word 
def find_content():
    pass


def replace_content():
    pass

################
# map funcs
edit_functions_list = {"Undo": undo_content,"Redo": redo_content ,"Cut": cut_content,"Copy":copy_content,"Paste":paste_content,"Find":find_content,"Replace":replace_content}

# Dropdown button
edit_menu_button = tk.Menubutton(top_bar,text="Edit",relief="raised",direction="below",bg= bg_color ,fg= font_color,activebackground= active_bg_top_color)

edit_files_menu = tk.Menu(edit_menu_button, tearoff=0,bg= bg_color ,fg= font_color,activebackground= active_bg_top_color )

for i in edit_functions_list :
    edit_files_menu.add_command(label=i,command=edit_functions_list[i]),edit_menu_button.config(menu=edit_files_menu),edit_menu_button.pack(side="left")



##########################

def always_on_top():
    global always_on_top_bool
    always_on_top_bool = not always_on_top_bool
    root.attributes("-topmost", always_on_top_bool)


def color():
    global current_dir 
    current_dir = cfg_file_path
    with open(cfg_file_path, 'r') as file:
        content = file.read()
        content_text.delete(1.0, tk.END)  # Clear  content
        content_text.insert(tk.END, content) # add content

def reset_color_cfg():
    pass


###################################

# map funcs
setting_functions_list = {"Always on top": always_on_top,"clear recent cache": clear_cache ,"color_config": color,"Reset color theme":reset_color_cfg}

# Dropdown button
setting_menu_button = tk.Menubutton(top_bar,text="Setting",relief="raised",direction="below",bg= bg_color,fg= font_color ,activebackground = active_bg_top_color)

setting_files_menu = tk.Menu(setting_menu_button, tearoff=0,bg= bg_color ,fg= font_color,activebackground= active_bg_top_color )

for i in setting_functions_list:
    setting_files_menu.add_command(label=i,command=setting_functions_list[i]),setting_menu_button.config(menu=setting_files_menu),setting_menu_button.pack(side="left")



#########################




# util for the um winder
top_bar.bind("<Button-1>", start_drag)
top_bar.bind("<B1-Motion>", drag_window)


resize_grip.bind("<Button-1>", start_resize)
resize_grip.bind("<B1-Motion>", resize_window)

content_text.bind("<Control-z>", lambda event: (undo_content(), "break")[1])
content_text.bind("<Control-x>", lambda event: (cut_content(), "break")[1])
content_text.bind("<Control-c>", lambda event: (copy_content(), "break")[1])
content_text.bind("<Control-v>", lambda event: (paste_content(), "break")[1])
content_text.bind("<Control-s>", lambda event: (save_content(), "break")[1])


#check_cache_recent_text()

root.mainloop()

if __name__ == '__main__':
    pass