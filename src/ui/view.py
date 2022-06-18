import tkinter
import tkinter as tk
import tkinter.filedialog as tkfd
import customtkinter as ctk
import crypto
import traceback
from typing import NoReturn


class MainView(ctk.CTk):
    def __init__(self, views: list) -> NoReturn:
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")
        ctk.CTk.__init__(self)
        self.columnconfigure(tuple(range(100)), weight=1)
        self.rowconfigure(tuple(range(100)), weight=1)
        self.frames = {}

        # center window
        self.geometry(self.get_geometry_string(
            500,
            900,
            ctk.CTk.winfo_screenheight(self),
            ctk.CTk.winfo_screenwidth(self)
        ))

        for view in views:
            self.frames[view.__name__] = view(self)

        ctk.CTk.report_callback_exception = self.show_error

        self.mainloop()


    def show_error(self, *args) -> NoReturn:
        err = traceback.format_exception(*args)
        tk.messagebox.showerror('Exception', err[-1])

    def get_geometry_string(self, window_height: int, window_width: int, screen_height: int, screen_width: int) -> str:
        x_coordinate = int((screen_width / 2) - (window_width / 2))
        y_coordinate = int((screen_height / 2) - (window_height / 2))
        return "{}x{}+{}+{}".format(window_width, window_height, x_coordinate, y_coordinate)


class SelectView(ctk.CTkFrame):
    def __init__(self, container: MainView) -> NoReturn:
        self.container = container
        ctk.CTkFrame.__init__(self, container)
        encrypt_button = ctk.CTkButton(master=self, text="Encrypt Files", command=self.select_file)
        decrypt_button = ctk.CTkButton(master=self, text="Decrypt Files", command=self.select_encrypted_file)
        self.grid(column=2, row=2, rowspan=96, columnspan=96, sticky=tk.NSEW)
        self.columnconfigure(tuple(range(10)), weight=1)
        self.rowconfigure(tuple(range(10)), weight=1)
        encrypt_button.grid(column=1, row=4, columnspan=8, sticky=tk.NSEW)
        decrypt_button.grid(column=1, row=6, columnspan=8, sticky=tk.NSEW)

    def select_file(self) -> NoReturn:
        self.files = tkfd.askopenfilenames()
        if len(self.files) > 0:
            self.container.frames["EncryptView"].tkraise()
            self.container.frames["EncryptView"].start()

    def select_encrypted_file(self) -> NoReturn:
        self.files = tkfd.askopenfilenames()
        if len(self.files) > 0:
            self.container.frames["DecryptView"].tkraise()
            self.container.frames["DecryptView"].start()


class EncryptView(ctk.CTkFrame):
    def __init__(self, container: MainView) -> NoReturn:
        self.container = container
        ctk.CTkFrame.__init__(self, container)
        self.grid(column=2, row=2, rowspan=96, columnspan=96, sticky=tk.NSEW)

        self.columnconfigure(tuple(range(10)), weight=1)
        self.rowconfigure(tuple(range(10)), weight=1)

        self.entry = ctk.CTkEntry(master=self, placeholder_text="Password...")
        self.entry.grid(column=1, row=2, columnspan=7, sticky=tk.NSEW)

        self.file_list = tk.Listbox(master=self, height=3, selectmode="multiple")
        self.file_list.grid(column=1, row=3, columnspan=7, sticky=tk.NSEW)

        self.remove_item_button = ctk.CTkButton(master=self, text="Remove selected elements", command=self.remove_items)
        self.remove_item_button.grid(column=8, row=3, sticky=tk.NSEW)

        generate_button = ctk.CTkButton(master=self, text="Generate", command=self.generate_password)
        generate_button.grid(column=8, row=2, sticky=tk.NSEW)

        button = ctk.CTkButton(master=self, text="Encrypt now", command=self.encrypt)
        button.grid(column=1, row=5, rowspan=3, columnspan=8, sticky=tk.NSEW)

        back_button = ctk.CTkButton(master=self, text="Back", command=self.back)
        back_button.grid(column=0, row=0, columnspan=10, sticky="NW")

    def start(self) -> NoReturn:
        # emtpy listbox
        self.file_list.delete(0, tkinter.END)
        for path in self.container.frames["SelectView"].files:
            self.file_list.insert(tk.END, path)

        # empty password input
        self.entry.delete(0, tk.END)

    def encrypt(self) -> NoReturn:
        paths = list(self.file_list.get(0, tk.END))

        password = str(self.entry.get())
        if len(password) < 4:
            raise Exception("Password not long enough")

        if not (dir := tk.filedialog.askdirectory()):
            return

        crypto.encrypt_files_by_path(paths, dir, password)

        tk.messagebox.showinfo(title="Encryption finished.", message="The Encryption has been finished.")
        self.container.frames["SelectView"].tkraise()

    def back(self) -> NoReturn:
        self.container.frames["SelectView"].tkraise()

    def generate_password(self) -> NoReturn:
        self.entry.delete(0, tk.END)
        self.entry.insert(0, crypto.generate_password(16))

    def remove_items(self) -> NoReturn:
        for entry in self.file_list.curselection():
            # do not delete the last item
            if self.file_list.size() > 1:
                self.file_list.delete(entry)


class DecryptView(ctk.CTkFrame):
    def __init__(self, container: MainView) -> NoReturn:
        self.container = container
        ctk.CTkFrame.__init__(self, container)
        self.grid(column=2, row=2, rowspan=96, columnspan=96, sticky=tk.NSEW)
        self.columnconfigure(tuple(range(10)), weight=1)
        self.rowconfigure(tuple(range(10)), weight=1)

        self.entry = ctk.CTkEntry(master=self, placeholder_text="Password...")
        self.entry.grid(column=1, row=2, columnspan=8, sticky=tk.NSEW)

        self.file_list = tk.Listbox(master=self, height=3, selectmode="multiple")
        self.file_list.grid(column=1, row=3, columnspan=7, sticky=tk.NSEW)

        self.remove_item_button = ctk.CTkButton(master=self, text="Remove selected elements", command=self.remove_items)
        self.remove_item_button.grid(column=8, row=3, sticky=tk.NSEW)

        button = ctk.CTkButton(master=self, text="Decrypt now", command=self.decrypt)
        button.grid(column=1, row=5, rowspan=3, columnspan=8, sticky=tk.NSEW)

        back_button = ctk.CTkButton(master=self, text="Back", command=self.back)
        back_button.grid(column=0, row=0, columnspan=10, sticky="NW")

    def start(self) -> NoReturn:
        # emtpy listbox
        self.file_list.delete(0, tkinter.END)

        for path in self.container.frames["SelectView"].files:
            self.file_list.insert(tk.END, path)

        # empty password input
        self.entry.delete(0, tk.END)

    def decrypt(self) -> NoReturn:
        paths = list(self.file_list.get(0, tk.END))

        password = str(self.entry.get())
        if len(password) < 4:
            raise Exception("Password not long enough")

        if not (dir := tk.filedialog.askdirectory()):
            return

        crypto.decrypt_files_by_path(paths, dir, password)
        tk.messagebox.showinfo(title="Decryption finished.", message="The Decrpytion has been finished.")
        self.container.frames["SelectView"].tkraise()

    def back(self) -> NoReturn:
        self.container.frames["SelectView"].tkraise()

    def remove_items(self) -> NoReturn:
        for entry in self.file_list.curselection():
            # do not delete the last item
            if self.file_list.size() > 1:
                self.file_list.delete(entry)
