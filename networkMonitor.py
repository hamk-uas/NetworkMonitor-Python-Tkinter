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

        # Creating treeview
        self.tree = ttk.Treeview(self.window, columns=("Process", "Upload speed", "Download speed", "Upload Usage", "Download Usage", "Total Usage"), show="headings")
        self.tree.heading("Process", text="Process")
        self.tree.heading("Upload speed", text="Upload speed")
        self.tree.heading("Download speed", text="Download speed")
        self.tree.heading("Upload Usage", text="Upload Usage")
        self.tree.heading("Download Usage", text="Download Usage")
        self.tree.heading("Total Usage", text="Total Usage")
        self.tree.column("Process", width=250, anchor="center")
        self.tree.column("Upload speed", width=150, anchor="center")
        self.tree.column("Download speed", width=150, anchor="center")
        self.tree.column("Upload Usage", width=150, anchor="center")
        self.tree.column("Download Usage", width=150, anchor="center")
        self.tree.column("Total Usage", width=150, anchor="center")
        self.tree.pack(fill="both", expand=True)

        self.last_counters = psutil.net_io_counters(pernic=True)
        self.refresh_delay = 1000

        self.data = []  # Displayed data

    # Converting bytes to other units
    def size(self, B):
        B = float(B)
        KB = float(1024)
        MB = float(KB ** 2)
        GB = float(KB ** 3)
        TB = float(KB ** 4)

        if B < KB:
            return f"{B} Bytes"
        elif KB <= B < MB:
            return f"{B/KB:.2f} KB"
        elif MB <= B < GB:
            return f"{B/MB:.2f} MB"
        elif GB <= B < TB:
            return f"{B/GB:.2f} GB"
        elif TB <= B:
            return f"{B/TB:.2f} TB"

    # Updating treeview
    def update_tree(self):
        if not self.is_measuring:
            return

        counters = psutil.net_io_counters(pernic=True)
        processes = psutil.process_iter(['pid', 'name'])
        process_data = {}

        for process in processes:
            pid = process.info['pid']
            name = process.info['name']
            process_data[pid] = {
                'name': name,
                'upload_speed': 0,
                'down_speed': 0,
                'upload_size': 0,
                'down_size': 0,
            }

        for interface, counter in counters.items():
            for conn in psutil.net_connections():
                pid = conn.pid
                if pid in process_data and (counter.bytes_sent - self.last_counters[interface].bytes_sent > 0 or counter.bytes_recv - self.last_counters[interface].bytes_recv > 0):
                    process_data[pid]['upload_speed'] += counter.bytes_sent - self.last_counters[interface].bytes_sent
                    process_data[pid]['down_speed'] += counter.bytes_recv - self.last_counters[interface].bytes_recv
                    process_data[pid]['upload_size'] += counter.bytes_sent
                    process_data[pid]['down_size'] += counter.bytes_recv

        self.last_counters = counters

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = SpeedMonitorApp()
    app.run()
