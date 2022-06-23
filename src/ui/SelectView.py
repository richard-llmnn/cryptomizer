import ui.EncryptView
import ui.DecryptView
import ui.AbstractView

import tkinter.filedialog as tkfd
import customtkinter as ctk
import tkinter as tk

from typing import NoReturn


class SelectView(ui.AbstractView.AbstractView):
    def __init__(self, container, storage) -> NoReturn:
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")
        super().__init__(container, storage)

        self.grid(column=2, row=2, rowspan=96, columnspan=96, sticky=tk.NSEW)
        # configure frame
        self.columnconfigure(tuple(range(10)), weight=1)
        self.rowconfigure(tuple(range(10)), weight=1)
        # encrypt button
        encrypt_button = ctk.CTkButton(
            master=self,
            text="Encrypt Files",
            command=self.show_encrypt_view
        )
        encrypt_button.grid(column=1, row=4, columnspan=8, sticky=tk.NSEW)
        # decrypt button
        decrypt_button = ctk.CTkButton(
            master=self,
            text="Decrypt Files",
            command=self.show_decrypt_view,
            fg_color="#1F6AA5",
            hover_color="#144870"
        )
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
