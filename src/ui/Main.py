import customtkinter as ctk
import traceback
import tkinter as tk
from typing import NoReturn
import ui.AbstractView
import ui.SelectView



class Main(ctk.CTk):
    def __init__(self) -> NoReturn:
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")
        super().__init__()
        # configure rows and columns
        self.columnconfigure(tuple(range(100)), weight=1)
        self.rowconfigure(tuple(range(100)), weight=1)
        # center window
        self.geometry(self.get_geometry_string(
            500,
            900,
            ctk.CTk.winfo_screenheight(self),
            ctk.CTk.winfo_screenwidth(self)
        ))
        self.title("Cryptomizer")
        # configure exception/error handling
        self.report_callback_exception = self.show_error
        # configure frames
        self.current_frame = None
        self.switch_frame(ui.SelectView.SelectView)
        # start tkinter eventloop
        self.mainloop()


    def show_error(self, *args) -> NoReturn:
        err = traceback.format_exception(*args)
        tk.messagebox.showerror('Exception', err[-1])
        print(err)

    def get_geometry_string(self, window_height: int, window_width: int, screen_height: int, screen_width: int) -> str:
        x_coordinate = int((screen_width / 2) - (window_width / 2))
        y_coordinate = int((screen_height / 2) - (window_height / 2))
        return "{}x{}+{}+{}".format(window_width, window_height, x_coordinate, y_coordinate)

    def switch_frame(self, frame: ui.AbstractView.AbstractView, storage: dict = {}) -> NoReturn:
        new_frame = frame(self, storage)
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = new_frame
        self.current_frame.start()
