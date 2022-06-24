import ui.EncryptView
import ui.DecryptView
import ui.AbstractView

import tkinter.filedialog as tkfd
import customtkinter as ctk
import tkinter as tk
import translation.Translator as tt

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
            text=tt.translate("encrypt.files"),
            command=self.show_encrypt_view
        )
        encrypt_button.grid(column=1, row=4, columnspan=8, sticky=tk.NSEW)
        # decrypt button
        decrypt_button = ctk.CTkButton(
            master=self,
            text=tt.translate("decrypt.files"),
            command=self.show_decrypt_view,
            fg_color="#1F6AA5",
            hover_color="#144870"
        )
        decrypt_button.grid(column=1, row=6, columnspan=8, sticky=tk.NSEW)
        # get all languages (the current language is at the first place)
        languages = tt.get_instance().get_languages()
        current_language = tt.get_instance().get_language_by_code(tt.get_current_language_code())
        languages.remove(current_language)
        languages.insert(0, current_language)
        # add language switcher
        self.language_switcher = ctk.CTkOptionMenu(
            master=self,
            values=languages,
            command=self.change_language
        )
        self.language_switcher.grid(column=8, row=0, columnspan=2, sticky=tk.N+tk.EW)

    def show_encrypt_view(self) -> NoReturn:
        self.files = tkfd.askopenfilenames(title=tt.translate("select.files.for.encryption"))
        if len(self.files) > 0:
            self.container.switch_frame(ui.EncryptView.EncryptView, {
                "files": self.files
            })

    def show_decrypt_view(self) -> NoReturn:
        self.files = tkfd.askopenfilenames(filetypes=[("CRYPT", ".crypt")], title=tt.translate("select.files.for.decryption"))
        if len(self.files) > 0:
            self.container.switch_frame(ui.DecryptView.DecryptView, {
                "files": self.files
            })

    def change_language(self, new_language: str) -> NoReturn:
        code = tt.get_instance().get_code_by_language(new_language)
        # english is the fallback language
        if code == None:
            code = "en_EN"

        tt.set_current_language_code(code)
        # re-render the frame in the new language
        self.container.switch_frame(ui.SelectView.SelectView)


    def start(self):
        pass
