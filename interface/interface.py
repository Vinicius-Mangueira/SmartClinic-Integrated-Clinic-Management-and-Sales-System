from tkinter import *

root = Tk()

class Application():
    def __init__(self):
        self.root = root
        self.tela()
        root.mainloop()
    def tela(self):
        self.root.title("SmartClinic - Integrated Clinic Management and Sales System")
        self.root.configure(background="#2A1313")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
Application()