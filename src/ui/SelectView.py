import tkinter.filedialog as tkfd
import customtkinter as ctk
from typing import NoReturn
import tkinter as tk
import ui.EncryptView
import ui.DecryptView
import ui.AbstractView


class SelectView(ui.AbstractView.AbstractView):
    def __init__(self, container, storage) -> NoReturn:
        super().__init__(container, storage)
        encrypt_button = ctk.CTkButton(master=self, text="Encrypt Files", command=self.show_encrypt_view)
        decrypt_button = ctk.CTkButton(master=self, text="Decrypt Files", command=self.show_decrypt_view)
        self.grid(column=2, row=2, rowspan=96, columnspan=96, sticky=tk.NSEW)
        self.columnconfigure(tuple(range(10)), weight=1)
        self.rowconfigure(tuple(range(10)), weight=1)
        encrypt_button.grid(column=1, row=4, columnspan=8, sticky=tk.NSEW)
        decrypt_button.grid(column=1, row=6, columnspan=8, sticky=tk.NSEW)

    def show_encrypt_view(self) -> NoReturn:
        self.files = tkfd.askopenfilenames()
        if len(self.files) > 0:
            self.container.switch_frame(ui.EncryptView.EncryptView, {
                "files": self.files
            })

    def show_decrypt_view(self) -> NoReturn:
        self.files = tkfd.askopenfilenames()
        if len(self.files) > 0:
            self.container.switch_frame(ui.DecryptView.DecryptView, {
                "files": self.files
            })

    def start(self):
        pass
