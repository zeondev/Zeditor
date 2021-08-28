import requests
from tkinter import *
from tkinter.filedialog import asksaveasfilename, askopenfilename, askopenfile
import tkinter.messagebox
import subprocess

# Vars
version = "0.1.0"

# Make window
root = Tk()
root.title("Zeditor")
file_path = ""

# Defs

def parseconf(fl):
    cfg = {}
    with open(fl) as cfile:
        # strip at newline
        # for l in lines
        #   splconf = split line at ":"
        #   cfg[splconf[0]] = splconf[1]
        lines = cfile.readlines()
        for l in lines:
            cstring = l.replace("\n", "")
            splconf = cstring.split(":")
            cfg[splconf[0]] = splconf[1]
    return cfg

colour_theme = parseconf("config/colourtheme.zc")
ext_lang_pairs = parseconf("config/lang.zc")
debuggers = parseconf("config/debug.zc")

def set_file_path(path):
    global file_path
    file_path = path

def save_as():
    if file_path == "":
        path = asksaveasfilename(filetypes=[("All Files", "*.*")])
    else:
        path = file_path
    with open(path, "w") as file:
        code = editor.get("1.0", END)
        file.write(code)
        set_file_path(path)

def open_file():
    path = askopenfilename(filetypes=[("All Files", "*.*")])
    with open(path, "r") as file:
        editor.delete("1.0", END)
        editor.insert("1.0", file.read())
        set_file_path(path)

def load_extension():
    path = askopenfilename(filetypes=[("All Files", "*.*")])
    with open(path, "r") as file:
        exec(file.read())

def get_file_extension(fpath):
    splitpath = fpath.split(".")
    return splitpath[len(splitpath) - 1]

def run():
    if file_path:
        # if debugger exists for language, use that debugger, else default to python
        # might change to just "execute the file"
        """ #needs fixing
        if get_file_extension(file_path) in ext_lang_pairs and ext_lang_pairs[get_file_extension(file_path)] in debuggers:
            command = f'{debuggers[ext_lang_pairs[get_file_extension(file_path)]]} {file_path}' 
        else:
            command = f'python {file_path}'
        """
        command = f'python {file_path}'
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
        output, error = process.communicate()
        code_out.delete("1.0", END)
        code_out.insert("1.0", output)
        code_out.insert("1.0", error)
    else:
        save_as()

def keybinds():
    keybinds = Toplevel(root)
    keybinds.geometry("750x250")
    keybinds.title("Keybinds")
    keybinds.configure(bg=colour_theme["popup_bg"])
    keybindsList = Label(keybinds, bg=colour_theme["popup_bg"], fg=colour_theme["popup_fg"], text="Ctrl+S: Save\nCtrl+R: Run program\nCtrl+O: Open File\nCtrl+K: Open keybinds")

    keybindsList.pack()

def about():
    about = Toplevel(root)
    about.geometry("750x250")
    about.title("About")
    about.configure(bg=colour_theme["popup_bg"])
    about1 = Label(about, bg=colour_theme["popup_bg"], fg=colour_theme["popup_fg"], text="Zeditor", font=("Consolas", 25))
    about2 = Label(about, bg=colour_theme["popup_bg"], fg=colour_theme["popup_fg"], text=f'Version {version}')

    about1.pack()
    about2.pack()

def codeHighlight():
    # editor.tag_config("start", foreground="red")
    # editor.tag_add("start", "1.6", "1.12")
    return 0

# Configure stuff
root.bind("<Control-s>", lambda x: save_as())
root.bind("<Control-r>", lambda x: run())
root.bind("<Control-k>", lambda x: keybinds())
root.bind("<Control-o>", lambda x: open_file())
root.bind("<Control-e>", lambda x: load_extension())
root.bind("<Key>", lambda x: codeHighlight())
menu_bar = Menu(root)

# File bar
file_bar = Menu(menu_bar, tearoff=0)
file_bar.add_command(label="Open", command=open_file)
file_bar.add_command(label="Save", command=save_as)
file_bar.add_command(label="Save As", command=save_as)
file_bar.add_command(label="Exit", command=exit)
file_bar.add_command(label="About", command=about)
menu_bar.add_cascade(label="File", menu=file_bar)

# Command Bar
option_bar = Menu(menu_bar, tearoff=0)
option_bar.add_command(label="Run", command=run)
option_bar.add_command(label="Keybinds", command=keybinds)
option_bar.add_command(label="Load Extension", command=load_extension)
menu_bar.add_cascade(label="Option", menu=option_bar)

# Tell window to add bar
root.config(menu=menu_bar)

# Make file bar

filebar = Listbox(root, height=100, width=15, bg=colour_theme["filebar_bg"], fg=colour_theme["filebar_fg"])

filebar.grid(row=0, column=0, sticky="nsew")
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Make editor

editor = Text(root, width=75, bg=colour_theme["editor_bg"], fg=colour_theme["editor_fg"], font="Consolas")

editor.grid(row=0, column=1, sticky="nsew")
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Output

code_out = Text(root, height=8, width=75, bg=colour_theme["out_bg"], fg=colour_theme["out_fg"], font="Consolas", state="normal")

code_out.grid(row=1, column=1, sticky="nsew")
root.grid_rowconfigure(1, weight=0)
root.grid_columnconfigure(0, weight=1)

# Open window
root.geometry("1100x750")
root.mainloop()