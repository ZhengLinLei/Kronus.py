
# TkinterAsync
# Zheng Lei - 2021 - Apache 2.0
# Github: https://github.com/ZhengLinLei/tkinterAsync
# PIP install: pip install tkinterAsync


import tkinter as tk
from tkinter import ttk
import threading

class Tkinter(threading.Thread):


    def __init__(self, fnc):
        threading.Thread.__init__(self)
        self.start()

        self.fnc = fnc

    def callback(self):
        self.root.quit()

    def run(self):
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.callback)

        # CALL OWN CODE
        self.fnc(self.root, tk, ttk)

        self.root.mainloop()
