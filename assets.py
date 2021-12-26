import tkinter as tk
from time import sleep 
from re import compile

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
    
    def resize_root(self, size):
        self.root.geometry(size) 

    def color_root(self, new_color): 
        self.root.config(background = new_color)
        
    def show_root(self): 
        self.root.mainloop() 

    def destroy_root(self): 
        self.root.destroy() 


class Email_msg: 
    def __init__(self, subject, message): 
        self.subject = subject 
        self.message = message 
    def get_msg(self): 
        return "Subject: " + self.subject + "\n\n" + self.message + "\n" 


def multiple_clock(n):                                                          
        if n % 50 == 0:                                                     # Every 50 emails 
            u = 60                              
            while u != 0:                                       
                print(f"Sleeping, {u} seconds left!")
                u-=1 
                sleep(1)                                                    # Wait 60s in total 
        else:                                                               # If not sleeping
            print(f"Email #{n} sent")
            sleep(0.6)                                                      # Send an email every 0.6s 


def pack_widgets(w_list):
    for widget in w_list: 
        widget.pack() 


def get_provider(s_email): 
    match = compile(r'@(.+).com')                            # Regex to find the provider from the email 
    try:    
        provider = match.search(s_email).group(1)            # Store it in the 'provider' variable 
    except AttributeError:                                      
        return None, None                                       # If this is called, then match didn't find anything (provider is None)
    else: 
        port = 587                                              # Storing the provider in their 'smtp' format and appropiate port
        if provider == 'hotmail' or provider == "outlook": smtp_s = 'smtp-mail.outlook.com'  

        elif provider == "gmail": smtp_s = 'smtp.gmail.com' 

        elif provider == 'yahoo': smtp_s = 'smtp.mail.yahoo.com'   

        elif provider == "att":
            smtp_s = 'smtp.mail.att.net'
            port = 465
        elif provider == "comcast": smtp_s = "smtp.comcast.net"      

        elif provider == "verizon": 
            smtp_s = "smtp.verizon.net"
            port = 465
        else: 
            return None, None                                 # If this is called, the provider is not supported yet
        return smtp_s, port 





