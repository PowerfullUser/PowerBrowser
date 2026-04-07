import os
import customtkinter as tk
from tkinter import messagebox as mbox

if not os.path.exists("Information"):
    os.mkdir("Information")

def set_theme(mode):
    with open("Information/theme", "w", encoding="utf-8") as w:
        w.write(str(mode))

def username():
    with open("Information/username", "w", encoding="utf-8") as w:
        text = name_var.get()
        w.write(text)

    mbox.showinfo("PowerBrowser v7 Setup","Setup successful")
    window.destroy()
    os.startfile("PowerBrowser.py")
    exit()

window = tk.CTk()
window.geometry("500x500")
window.minsize(500, 500)
window.maxsize(500, 500)

tk.CTkLabel(window, text="PowerBrowser v7 Setup", font=("Segoe UI", 20)).pack()

tk.CTkLabel(window, text="", font=("Segoe UI", 14)).pack()

tk.CTkLabel(window, text="Select the desired mode for your browser", font=("Segoe UI", 14)).pack()

frame = tk.CTkFrame(window)

dark_mode = tk.CTkButton(frame, text="Dark Mode", font=("Segoe UI", 14), command=lambda: set_theme("d"))
dark_mode.pack(side="left", padx=5)

light_mode = tk.CTkButton(frame, text="Light Mode", font=("Segoe UI", 14), command=lambda: set_theme("l"))
light_mode.pack(side="left", padx=5)

frame.pack()

tk.CTkLabel(window, text="", font=("Segoe UI", 14)).pack()

tk.CTkLabel(window, text="What do you want PowerBrowser v7 to call you?", font=("Segoe UI", 14)).pack()

name_var = tk.StringVar()
name_input = tk.CTkEntry(window, textvariable=name_var, width=350, font=("Segoe UI", 14))
name_input.pack()

tk.CTkLabel(window, text="", font=("Segoe UI", 14)).pack()

finish_button = tk.CTkButton(window, text="Finish Setup", font=("Segoe UI", 14), command=lambda: username())
finish_button.pack()

window.mainloop()
