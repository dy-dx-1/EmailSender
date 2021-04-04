import smtplib 
import tkinter as tk
import re
import classes 

# ENTER EMAIL FIRST 
email = "PLACEHOLDER"   ######################################################################################
match = re.compile(r'@(.+)')
connect = smtplib.SMTP('smtp.'+match.search(email).group(1), 587) # setting up connection 
connect.ehlo()  # starting connection
connect.starttls()   # starting encryption before login 

root = classes.TkinterWindow('main', 'Email sender', '500x400') 
root.construct_root()

PassLabel = tk.Label(text = "Password for the email "+ email + ' : ')
Pass_Entry = tk.Entry(width = 30, show = "*") 

def login(): 
    try:
        key = str(Pass_Entry.get())
        connect.login(email, key) # login
        PassLabel.configure(text = "Logged in!")
        Pass_Entry.delete(0, 'end')
        button_password.configure(state = tk.DISABLED) 
        
    except smtplib.SMTPAuthenticationError:  
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
    receiver_email = str(Receiver_Entry.get())
    Subject = str(Subject_Entry.get()) 
    Content = str(Content_Entry.get())
    message = "Subject: " + Subject + "\n\n" + Content + "\n" 
    connect.sendmail(email, receiver_email, message)
    connect.quit() 
    root.destroy_root()
    

button_launch = tk.Button(text = "Press to send the emails", command = get_info) 

PassLabel.pack()
Pass_Entry.pack()
button_password.pack()
Receiver_Label.pack()
Receiver_Entry.pack()
Subject_Label.pack()
Subject_Entry.pack()
Content_Label.pack()
Content_Entry.pack()
button_launch.pack()
root.show_root() 



