import tkinter as tk
from tkinter import Canvas, PhotoImage
import subprocess

class FlowerDesignerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Flower Designer Mode Selector")

        self.bg_image = PhotoImage(file="top.png")
        self.canvas = Canvas(root, width=self.bg_image.width(), height=self.bg_image.height())
        self.canvas.pack(fill="both", expand=True)

        self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image)

        self.title_label = tk.Label(root, text="Flower Designer", font=("Arial", 60), fg="white", bg="black")
        self.title_label_window = self.canvas.create_window(self.bg_image.width()//2, 50, anchor="n", window=self.title_label)

        self.button_c = tk.Button(root, text="Sympetalous flower mode", command=self.toggle_flower_designer_c, font=("Arial", 20), fg="white", bg="black")
        self.button_c_window = self.canvas.create_window(self.bg_image.width()//2, 400, anchor="n", window=self.button_c)

        self.button_dc = tk.Button(root, text="Polypetalous flowers mode", command=self.toggle_flower_designer_dc, font=("Arial", 20), fg="white", bg="black")
        self.button_dc_window = self.canvas.create_window(self.bg_image.width()//2, 500, anchor="n", window=self.button_dc)

        self.c_running = False
        self.c_process = None

        self.dc_running = False
        self.dc_process = None

    def toggle_flower_designer_c(self):
        if self.c_running:
            self.c_process.terminate()
            self.c_process = None
            self.c_running = False
            self.button_c.config(text="Sympetalous flower mode")
        else:
            self.c_process = subprocess.Popen(['python3', 'flower_designer_c.py'])
            self.c_running = True
            self.button_c.config(text="Sympetalous flower mode running...")

    def toggle_flower_designer_dc(self):
        if self.dc_running:
            self.dc_process.terminate()
            self.dc_process = None
            self.dc_running = False
            self.button_dc.config(text="Polypetalous flowers mode")
        else:
            self.dc_process = subprocess.Popen(['python3', 'flower_designer_dc.py'])
            self.dc_running = True
            self.button_dc.config(text="Polypetalous flowers mode running...")

if __name__ == "__main__":
    root = tk.Tk()
    app = FlowerDesignerApp(root)
    root.geometry(f"{app.bg_image.width()}x{app.bg_image.height()}")
    root.mainloop()
