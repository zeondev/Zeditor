import requests
from tkinter import *
from tkinter.filedialog import asksaveasfilename, askopenfilename
import tkinter.messagebox
import subprocess

# Vars
version = "0.1.0"

# Make window
root = Tk()
root.title("Zeditor")
file_path = ""

# Defs

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


def run():
    if file_path:
        command = f'python {file_path}'
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
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
    keybinds.configure(bg="#313131")
    keybindsList = Label(keybinds, bg="#313131", fg="#ffffff", text="Ctrl+S: Save\nCtrl+R: Run program\nCtrl+O: Open File\nCtrl+K: Open keybinds")

    keybindsList.pack()

def about():
    about = Toplevel(root)
    about.geometry("750x250")
    about.title("About")
    about.configure(bg="#313131")
    about1 = Label(about, bg="#313131", fg="#ffffff", text="Zeditor", font=("Consolas", 25))
    about2 = Label(about, bg="#313131", fg="#ffffff", text=f'Version {version}')

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

# Make editor

editor = Text(root, width=100, bg="#313131", fg="#ffffff", font="Consolas")

editor.grid(row=0, column=0, sticky="nsew")
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Output

code_out = Text(root, height=8, width=100, bg="#313131", fg="#ffffff", font="Consolas", state="normal")

code_out.grid(row=1, column=0, sticky="nsew")
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Open window
root.geometry("1100x750")
root.mainloop()