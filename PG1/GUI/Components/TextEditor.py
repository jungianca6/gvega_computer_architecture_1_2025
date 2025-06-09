import tkinter as tk


class TextEditor(tk.Text):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.config(font=("Noto Serif", 16), bg="#BBDEFB", fg="black", wrap=tk.WORD, undo=True,
                    insertbackground="#0D47A1")

        self.bind("<Control-c>", self.copy)
        self.bind("<Control-v>", self.paste)
        self.bind("<Control-a>", self.select_all)
        self.bind("<Control-z>", self.undo)

    def copy(self, event=None):
        try:
            self.clipboard_clear()
            text = self.get("sel.first", "sel.last")
            self.clipboard_append(text)
        except tk.TclError:
            pass

        return "break"

    def paste(self, event=None):
        try:
            text = self.selection_get(selection="CLIPBOARD")
            self.insert(tk.INSERT, text)
        except tk.TclError:
            pass

        return "break"

    def select_all(self, event=None):
        self.tag_add(tk.SEL, "1.0", tk.END)
        self.mark_set(tk.INSERT, "1.0")
        self.see(tk.INSERT)

        return "break"

    def undo(self, event=None):
        try:
            self.edit_undo()
        except tk.TclError:
            pass

        return "break"


