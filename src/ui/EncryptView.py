import crypto
import customtkinter as ctk
from typing import NoReturn
import tkinter as tk
import ui.AbstractView
import ui.SelectView


class EncryptView(ui.AbstractView.AbstractView):
    def __init__(self, container, storage) -> NoReturn:
        super().__init__(container, storage)
        self.grid(column=2, row=2, rowspan=96, columnspan=96, sticky=tk.NSEW)

        self.columnconfigure(tuple(range(10)), weight=1)
        self.rowconfigure(tuple(range(10)), weight=1)

        # back button
        back_button = ctk.CTkButton(master=self, text="Back", command=self.back)
        back_button.grid(column=0, row=0, columnspan=10, sticky="NW")
        # password input field
        self.entry = ctk.CTkEntry(master=self, placeholder_text="Password...")
        self.entry.grid(column=1, row=1, columnspan=7, sticky=tk.NSEW)
        # generate password button
        generate_button = ctk.CTkButton(master=self, text="Generate", command=self.generate_password)
        generate_button.grid(column=8, row=1, sticky=tk.NSEW)
        # file list box
        self.file_list = tk.Listbox(master=self, height=1, selectmode="multiple")
        self.file_list.grid(column=1, row=3, columnspan=7, rowspan=4, sticky=tk.NSEW)
        # remove file from list-box button
        self.remove_item_button = ctk.CTkButton(
            master=self,
            text="Remove selected elements",
            command=self.remove_items,
            fg_color="red",
            hover_color="#ff5555"
        )
        self.remove_item_button.grid(column=8, row=3, rowspan=4, sticky=tk.NSEW)
        # start encryption button
        button = ctk.CTkButton(master=self, text="Encrypt now", command=self.encrypt)
        button.grid(column=1, row=8, rowspan=1, columnspan=8, sticky=tk.NSEW)

    def start(self) -> NoReturn:
        for path in self.storage.get("files"):
            self.file_list.insert(tk.END, path)

    def encrypt(self) -> NoReturn:
        paths = list(self.file_list.get(0, tk.END))

        password = str(self.entry.get())
        if len(password) < 4:
            raise Exception("Password not long enough")

        if not (dir := tk.filedialog.askdirectory()):
            return

        crypto.encrypt_files_by_path(paths, dir, password)

        tk.messagebox.showinfo(title="Encryption finished.", message="The Encryption has been finished.")
        self.container.switch_frame(ui.SelectView.SelectView)

    def back(self) -> NoReturn:
        self.container.switch_frame(ui.SelectView.SelectView)

    def generate_password(self) -> NoReturn:
        self.entry.delete(0, tk.END)
        self.entry.insert(0, crypto.generate_password(16))

    def remove_items(self) -> NoReturn:
        for entry in self.file_list.curselection():
            # do not delete the last item
            if self.file_list.size() > 1:
                self.file_list.delete(entry)
