from tkinter import *
from tkinter.filedialog import asksaveasfilename, askopenfilename
import tkinter.messagebox
import subprocess

# Make window
root = Tk()
root.title("Zeditor")
root.geometry("1100x750")
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

def run():
    if file_path:
        command = f'python {file_path}'
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, error = process.communicate()
        code_out.insert("1.0", output)
        code_out.insert("1.0", error)
    else:
        save_as()
def keybinds():
    top = Toplevel(root)
    top.geometry("750x250")
    top.title("Keybinds")
    keybindsList = Label(top, text="Ctrl+S: Save\nCtrl+R: Run program\nCtrl+O: Open File\nCtrl+K: Open keybinds")
    keybindsList.pack()

# Configure stuff
root.bind("<Control-s>", lambda x: save_as())
root.bind("<Control-r>", lambda x: run())
root.bind("<Control-k>", lambda x: keybinds())
root.bind("<Control-o>", lambda x: open_file())
menu_bar = Menu(root)

# File bar
file_bar = Menu(menu_bar, tearoff=0)
file_bar.add_command(label="Open", command=open_file)
file_bar.add_command(label="Save", command=save_as)
file_bar.add_command(label="Save As", command=save_as)
file_bar.add_command(label="Exit", command=exit)
menu_bar.add_cascade(label="File", menu=file_bar)

# Command Bar
option_bar = Menu(menu_bar, tearoff=0)
option_bar.add_command(label="Run", command=run)
option_bar.add_command(label="Keybinds", command=keybinds)
menu_bar.add_cascade(label="Option", menu=option_bar)

# Tell window to add bar
root.config(menu=menu_bar)

# Make editor

editor = Text(root, width=100, bg="#313131", fg="#ffffff", font="Consolas")
editor.pack()

code_out = Text(root, height=8, width=100, bg="#313131", fg="#ffffff", font="Consolas", state="normal")
code_out.pack()

# Open window
root.mainloop()


