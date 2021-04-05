import smtplib 
import tkinter as tk
import re
import classes 

root = classes.TkinterWindow('main', 'Email sender', '500x400') 
root.construct_root()

sender_email_Label = tk.Label(text = "Your email address: ") 
sender_email_Entry = tk.Entry(width = 30)
PassLabel = tk.Label(text = "Password for the email: ")
Pass_Entry = tk.Entry(width = 30, show = "*") 

def get_provider(): 
    match = re.compile(r'@(.+).com') 
    try:  
        provider = match.search(sender_email).group(1) 
    except AttributeError: 
        return None, None 
    else: 
        port = 587
        if provider == 'hotmail' or provider == "outlook":
            smtp_s = 'smtp-mail.outlook.com' 
        elif provider == "gmail": 
            smtp_s = 'smtp.gmail.com' 
        elif provider == 'yahoo':
            smtp_s = 'smtp.mail.yahoo.com'
        elif provider == "att":
            smtp_s = 'smtp.mail.att.net'
            port = 465
        elif provider == "comcast": 
            smtp_s = "smtp.comcast.net" 
        elif provider == "verizon": 
            smtp_s = "smtp.verizon.net"
            port = 465
        
        return smtp_s, port 

        
def login(): 
    global sender_email 
    global connect 
    sender_email = sender_email_Entry.get()      
    smtp_server, port = get_provider()  # Getting sender email address 
    if (smtp_server, port) == (None, None): 
        sender_email_Label.configure(text = "Sorry that email provider is not supported")                 
 
    else: 
        connect = smtplib.SMTP(smtp_server, port)                                # setting up connection 
        connect.ehlo()                                                           # starting connection
        connect.starttls()                                                       # starting encryption before login
        try:                                                                     # First attempting log in 
            key = Pass_Entry.get()                                               # Getting password 
            connect.login(sender_email, key)                                     # Logging in 
            
        except smtplib.SMTPAuthenticationError:                                  # If the password is incorrect 
            PassLabel.configure(text = "Wrong password, try again")
            Pass_Entry.delete(0, 'end')                                          # Clear the entry 
        
        else:                                                                    # If log in was successful 
            PassLabel.configure(text = "Logged in!")                             
            button_password.configure(state = tk.DISABLED)                       # Disable button to log in 

            Receiver_Label.pack()                                                
            Receiver_Entry.pack()
            Subject_Label.pack()
            Subject_Entry.pack()
            Content_Label.pack()
            Content_Entry.pack()
            button_launch.pack()                                                 # Let the message creation entries appear 

button_password = tk.Button(text = "Log in", command = login)
Receiver_Label = tk.Label(text = "To who do you want to send the emails to?")
Receiver_Entry = tk.Entry(width = 30) 
Subject_Label = tk.Label(text = "Enter the subject of the email: ")
Subject_Entry = tk.Entry() 
Content_Label = tk.Label(text = "Enter the message in the email: ") 
Content_Entry = tk.Entry() 

def send_emails():
    receiver_email = Receiver_Entry.get()

    message = classes.email(Subject_Entry.get(), Content_Entry.get()).get_msg()

    connect.sendmail(sender_email, receiver_email, message)
    connect.quit() 
    root.destroy_root()
    
button_launch = tk.Button(text = "Press to send the emails", command = send_emails) 

sender_email_Label.pack() 
sender_email_Entry.pack()
PassLabel.pack()
Pass_Entry.pack()
button_password.pack()
root.show_root() 



