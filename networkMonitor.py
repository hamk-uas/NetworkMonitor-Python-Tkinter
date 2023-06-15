import psutil
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle

# Tkinter interface
class SpeedMonitorApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Speed Monitor")
        self.window.geometry("1000x600")
        self.window.resizable(width=False, height=True)

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = SpeedMonitorApp()
    app.run()
