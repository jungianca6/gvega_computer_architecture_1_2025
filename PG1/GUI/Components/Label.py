import tkinter as tk


class Label(tk.Label):
    def __init__(self, master=None, text="", style_type="Text", **kwargs):
        super().__init__(master, text=text)

        if style_type == "Title":
            self.config(font=("Arial", 20, "bold"), fg="white", bg="#1976D2")

        elif style_type == "Subtitle":
            self.config(font=("Arial", 16, "bold"), fg="white", bg="#1976D2")

        elif style_type == "Warning":
            self.config(font=("Arial", 10, "bold"), fg="white", bg="#0D47A1")

        elif style_type == "List":
            self.config(font=("Arial", 16), bg="#3B5998", fg="white",
                        bd=2, relief="raised", padx=5, pady=5,
                        width=20, anchor='w')

        else:  # "Text" por defecto
            self.config(font=("Arial", 12), fg="black", bg="#E3F2FD")

    def SetText(self, text):
        self.config(text=text)

