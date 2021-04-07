import tkinter as tk
class TkinterWindow:
    # root refers to the main window name (usually main or root) 
    def __init__(self, root, title_, size = '500x500', background_color = '#d4cfcf'): 
        self.root = root                   # for example, self.root is the actual name (we are putting it equal to the
        self.title_ = title_               # variable 'root' that will be called when creating and then self.root will hold the value)        
        self.size = size              
        self.background_color = background_color 
        
    def construct_root(self): 
        self.root = tk.Tk() 
        self.root.title(self.title_)
        self.root.geometry(self.size)
        self.root.config(background = self.background_color)
        
    def show_root(self): 
        self.root.mainloop() 

    def destroy_root(self): 
        self.root.destroy() 

class email_msg: 
    def __init__(self, subject, message): 
        self.subject = subject 
        self.message = message 
    def get_msg(self): 
        return "Subject: " + self.subject + "\n\n" + self.message + "\n"  # Uhhh don't remember if that last \n is necessary 
