import customtkinter as ctk


class AbstractView(ctk.CTkFrame):
    def __init__(self, container, storage):
        super().__init__(master=container)
        self.container = container
        self.storage = storage
