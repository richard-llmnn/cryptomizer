import tkinter as tk
import tkinter.filedialog as tkfd
import customtkinter as ctk
import crypto
import traceback

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
        
        ctk.CTk.report_callback_exception = self.show_error

        self.mainloop()
    
    def show_error(self, *args):
        err = traceback.format_exception(*args)
        tk.messagebox.showerror('Exception',err[-1])

class SelectView(ctk.CTkFrame):
    def __init__(self, container):
        self.container = container
        ctk.CTkFrame.__init__(self, container)
        encrypt_button = ctk.CTkButton(master=self, text="Encrypt Files", command=self.select_file)
        decrypt_button = ctk.CTkButton(master=self, text="Decrypt Files", command=self.select_encrypted_file)
        self.grid(column=2, row=2, rowspan=96, columnspan=96, sticky=tk.NSEW)
        self.columnconfigure(tuple(range(10)), weight=1)
        self.rowconfigure(tuple(range(10)), weight=1)
        encrypt_button.grid(column=1, row=4, columnspan=8, sticky=tk.NSEW)
        decrypt_button.grid(column=1, row=6, columnspan=8, sticky=tk.NSEW)

    def select_file(self):
        self.files = tkfd.askopenfilenames()
        if len(self.files) > 0:
            self.container.frames["EncryptView"].tkraise()

    def select_encrypted_file(self):
        self.files = tkfd.askopenfilenames()
        if len(self.files) > 0:
            self.container.frames["DecryptView"].tkraise()

class EncryptView(ctk.CTkFrame):
    def __init__(self, container):
        self.container = container
        ctk.CTkFrame.__init__(self, container)
        self.grid(column=2, row=2, rowspan=96, columnspan=96, sticky=tk.NSEW)
        self.columnconfigure(tuple(range(10)), weight=1)
        self.rowconfigure(tuple(range(10)), weight=1)
        self.entry = ctk.CTkEntry(master=self, placeholder_text="Password...")
        self.entry.grid(column=1, row=2, columnspan=7, sticky=tk.NSEW)
        generate_button = ctk.CTkButton(master=self, text="Generate", command=self.generate_password)
        generate_button.grid(column=8, row=2, sticky=tk.NSEW)
        button = ctk.CTkButton(master=self, text="Encrypt now", command=self.encrypt)
        button.grid(column=1, row=4, rowspan=3, columnspan=8, sticky=tk.NSEW)
        back_button = ctk.CTkButton(master=self, text="Back", command=self.back)
        back_button.grid(column=0, row=0, columnspan=10, sticky="NW")
    
    def encrypt(self):
        if not (dir := tk.filedialog.askdirectory()):
            return
        password = self.entry.get()
        crypto.encrypt_files_by_path(list(self.container.frames["SelectView"].files), dir, password)
        tk.messagebox.showinfo(title="Encryption finished.", message="The Encryption has been finished.")
        self.container.frames["SelectView"].tkraise()
    
    def back(self):
        self.container.frames["SelectView"].tkraise()

    def generate_password(self):
        self.entry.delete(0,tk.END)
        self.entry.insert(0,crypto.generate_password(16))


class DecryptView(ctk.CTkFrame):
    def __init__(self, container):
        self.container = container
        ctk.CTkFrame.__init__(self, container)
        self.grid(column=2, row=2, rowspan=96, columnspan=96, sticky=tk.NSEW)
        self.columnconfigure(tuple(range(10)), weight=1)
        self.rowconfigure(tuple(range(10)), weight=1)
        self.entry = ctk.CTkEntry(master=self, placeholder_text="Password...")
        self.entry.grid(column=1, row=2, columnspan=8, sticky=tk.NSEW)
        button = ctk.CTkButton(master=self, text="Decrypt now", command=self.decrypt)
        button.grid(column=1, row=4, rowspan=3, columnspan=8, sticky=tk.NSEW)
        back_button = ctk.CTkButton(master=self, text="Back", command=self.back)
        back_button.grid(column=0, row=0, columnspan=10, sticky="NW")
    
    def decrypt(self):
        if not (dir := tk.filedialog.askdirectory()):
            return
        password = self.entry.get()
        crypto.decrypt_files_by_path(list(self.container.frames["SelectView"].files), dir, password)
        tk.messagebox.showinfo(title="Decryption finished.", message="The Decrpytion has been finished.")
        self.container.frames["SelectView"].tkraise()
    
    def back(self):
        self.container.frames["SelectView"].tkraise()
