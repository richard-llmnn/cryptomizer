import tkinter as tk
import tkinter.filedialog as tkfd
import customtkinter as ctk
import crypto

class MainView(ctk.CTk):
    def __init__(self, *views):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")
        ctk.CTk.__init__(self)
        self.columnconfigure(tuple(range(100)), weight=1)
        self.rowconfigure(tuple(range(100)), weight=1)
        self.geometry("400x240")
        self.frames = {}

        for view in views:
            self.frames[view.__name__] = view(self)

        self.mainloop()

class SelectView(ctk.CTkFrame):
    def __init__(self, container):
        self.container = container
        ctk.CTkFrame.__init__(self, container)
        button = ctk.CTkButton(master=self, text="Select File", command=self.select_file)
        self.grid(column=25, row=25, rowspan=50, columnspan=50, sticky=tk.NSEW)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        button.grid(column=0, row=0, sticky=tk.NSEW)

    def select_file(self):
        self.files = tkfd.askopenfilenames()
        self.container.frames["EncryptView"].tkraise()

class EncryptView(ctk.CTkFrame):
    def __init__(self, container):
        self.container = container
        ctk.CTkFrame.__init__(self, container)
        self.grid(column=25, row=25, rowspan=50, columnspan=50, sticky=tk.NSEW)
        self.columnconfigure(tuple(range(10)), weight=1)
        self.rowconfigure(tuple(range(10)), weight=1)
        self.entry = ctk.CTkEntry(master=self, placeholder_text="Password...")
        self.entry.grid(column=1, row=3, columnspan=8, sticky=tk.NSEW)
        button = ctk.CTkButton(master=self, text="Encrypt", command=self.encrypt)
        button.grid(column=1, row=5, rowspan=3, columnspan=8, sticky=tk.NSEW)
    
    def encrypt(self):
        password = self.entry.get()
        crypto.encrypt_files_by_path(list(self.container.frames["SelectView"].files), "/tmp", password)

