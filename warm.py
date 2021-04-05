import smtplib 
import tkinter as tk
import re
import classes 

# ENTER EMAIL FIRST 
sender_email = "PLACEHOLDER"   ######################################################################################
match = re.compile(r'@(.+)')  # to get the smtp from the email ; NEED ADD SUPPORT FOR OTHER PORTS AND EMAIL TYPES 

connect = smtplib.SMTP('smtp.'+match.search(sender_email).group(1), 587) # setting up connection 
connect.ehlo()  # starting connection
connect.starttls()   # starting encryption before login 

root = classes.TkinterWindow('main', 'Email sender', '500x400') 
root.construct_root()

PassLabel = tk.Label(text = "Password for the email "+ sender_email + ' : ')
Pass_Entry = tk.Entry(width = 30, show = "*") 

def login(): 
    try:                                # First attempting log in 
        key = Pass_Entry.get()
        connect.login(sender_email, key) 
        PassLabel.configure(text = "Logged in!")
        button_password.configure(state = tk.DISABLED)    
        Receiver_Label.pack()
        Receiver_Entry.pack()
        Subject_Label.pack()
        Subject_Entry.pack()
        Content_Label.pack()
        Content_Entry.pack()
        button_launch.pack()
           
    except smtplib.SMTPAuthenticationError:   # If the password is incorrect 
        PassLabel.configure(text = "Wrong password, try again")
        Pass_Entry.delete(0, 'end')
        
button_password = tk.Button(text = "Log in", command = login)
Receiver_Label = tk.Label(text = "To who do you want to send the emails to?")
Receiver_Entry = tk.Entry(width = 30) 
Subject_Label = tk.Label(text = "Enter the subject of the email: ")
Subject_Entry = tk.Entry() 
Content_Label = tk.Label(text = "Enter the message in the email: ") 
Content_Entry = tk.Entry() 

def get_info():
    receiver_email = Receiver_Entry.get()

    message = classes.email(Subject_Entry.get(), Content_Entry.get()).get_msg()

    connect.sendmail(sender_email, receiver_email, message)
    connect.quit() 
    root.destroy_root()
    

button_launch = tk.Button(text = "Press to send the emails", command = get_info) 

PassLabel.pack()
Pass_Entry.pack()
button_password.pack()
root.show_root() 



