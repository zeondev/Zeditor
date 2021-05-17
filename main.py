from tkinter import *
from tkinter.filedialog import asksaveasfilename, askopenfilename
import subprocess

# Make window
compiler = Tk()
compiler.title("Zeditor")
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

# Configure menu bar
menu_bar = Menu(compiler)

# File bar
file_bar = Menu(menu_bar, tearoff=0)
file_bar.add_command(label="Open", command=open_file)
file_bar.add_command(label="Save", command=save_as)
file_bar.add_command(label="Save As", command=save_as)
file_bar.add_command(label="Exit", command=exit)
menu_bar.add_cascade(label="File", menu=file_bar)

# Command Bar
cmd_bar = Menu(menu_bar, tearoff=0)
cmd_bar.add_command(label="Run", command=run)
menu_bar.add_cascade(label="Command", menu=cmd_bar)

# Tell window to add bar
compiler.config(menu=menu_bar)

# Make editor
editor = Text()
editor.pack()

code_out = Text(height=8)
code_out.pack()

# Open window
compiler.mainloop()