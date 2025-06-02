import tkinter as tk


class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None

        self.widget.bind("<Enter>", self.show_tip)
        self.widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        if self.tip_window or not self.text:
            return
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5

        # Crear la ventana flotante
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)  # sin bordes
        tw.wm_geometry(f"+{x}+{y}")

        label = tk.Label(tw, text=self.text, bg="#BBDEFB", fg="black",
                         relief=tk.SOLID, borderwidth=1,
                         font=("Arial", "8", "normal"))
        label.pack(ipadx=4)

    def hide_tip(self, event=None):
        tw = self.tip_window
        self.tip_window = None
        if tw:
            tw.destroy()