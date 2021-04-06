import smtplib 
import tkinter as tk
import re
import classes 
from time import sleep 


def get_provider(): 
    match = re.compile(r'@(.+).com')                            # Regex to find the provider from the email 
    try:    
        provider = match.search(sender_email).group(1)          # Store it in the 'provider' variable 
    except AttributeError:                                      
        return None, None                                       # If this is called, then match didn't find anything (provider is None)
    else: 
        port = 587                                              # Storing the provider in their 'smtp' format and appropiate port
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
        else: 
            return None, None                                 # If this is called, the provider is not supported yet
        
        return smtp_s, port 

        
def login(): 
    global sender_email                                                         # Global variables to reuse them in send_emails() 
    global connect 
    sender_email = sender_email_Entry.get()                                     # Getting sender email 

    (smtp_server, port) = get_provider()                                        # Getting the provider and the appropiate port

    if (smtp_server, port) == (None, None):                                     # if nothing is returned, get_provider() didn't find a supported email
        sender_email_Label.configure(text = "Sorry that email provider is not supported")                 
    else: 
        connect = smtplib.SMTP(smtp_server, port)                               # setting up connection 
        connect.ehlo()                                                          # starting connection
        connect.starttls()                                                      # starting encryption before login
        try:                                                                    # First attempting log in 
            key = Pass_Entry.get()                                              # Getting password 
            connect.login(sender_email, key)                                    # Logging in 
            
        except smtplib.SMTPAuthenticationError:                                 # If the password is incorrect 
            PassLabel.configure(text = "Wrong password, try again")
            Pass_Entry.delete(0, 'end')                                         # Clear the entry 
        
        else:                                                                   # If log in was successful 
            PassLabel.configure(text = "Logged in!")                             
            button_password.configure(state = tk.DISABLED)                      # Disable button to log in 

            Receiver_Label.pack()                                                
            Receiver_Entry.pack()
            Subject_Label.pack()
            Subject_Entry.pack()
            Content_Label.pack()
            Content_Entry.pack()
            button_launch.pack(side = tk.LEFT)                                  # Let the message creation entries appear 
            button_spam.pack(side = tk.RIGHT)                                   # Let the 'spam mode' button appear 

def send_emails(q):                                                             
    receiver_email = Receiver_Entry.get()                                       # Getting receiver email 
    try:
        q = int(float(q))                                                       # If float is inputed, convert to int 
    except ValueError:                                                      
        count_label.configure(text = "Email count must be an integer!")         # If str is inputed ValueError will be raised 
    else:
        if q>1000 or q<=0:                                                      # If person inputed too large number or a negative number
            count_label.configure(text = "Email count must be between 0 and 1000!")

        else: 
            if spam_mode == 1:                                                  # If the spam mode is on 
                for n in range(1, q+1):                                         # Send the multiple emails
                    message = classes.email(Subject_Entry.get()+str(n),
                     Content_Entry.get()).get_msg()                         # Add a number to the title to prevent email merging emails in one
                    connect.sendmail(sender_email, receiver_email, message) # Send the mail 
                    spam_clock(n)                                           # Run the clock to avoid blocking from provider 

            else:                                                                 #If spam mode is off 
                message = classes.email(Subject_Entry.get(), Content_Entry.get()).get_msg() # Getting message (without number this time)
                connect.sendmail(sender_email, receiver_email, message)                     # Send email 
            connect.quit()                                                  # Disconnect from service 
            root.destroy_root()                                             # Destroy window and close program 

def spam_clock(n):                                                          
        if n % 50 == 0:                                                     # Every 50 emails 
            u = 60                              
            while u != 0:                                       
                count_label.configure(text = "Sleeping, " + str(u) + " seconds left!")
                u-=1 
                sleep(1)                                                    # Wait 60s in total 
        else:                                                               # If not sleeping
            count_label.configure(text = "Email #"+ str(n) +"sent")
            sleep(0.6)                                                      # Send an email every 0.6s 

def activate_spam():                                                        # Turning spam mode on and off 
    global spam_mode                                                        # Global to call it in send_emails() 
    spam_mode = spam_mode*-1                                                
    if spam_mode == 1:                                                      
        count_label.pack()                                                   
        count_entry.pack()                                                  # Make the spam mode settings appear when on 
    else: 
        count_label.pack_forget()
        count_entry.pack_forget()                                           # Remove the settings if spam mode is off 



root = classes.TkinterWindow('main', 'Email sender', '700x300')             # Setting up window settings 
root.construct_root()                                                       # Creating window 

sender_email_Label = tk.Label(text = "Your email address: ")                
sender_email_Entry = tk.Entry(width = 30)                                   # Entering sender email 
PassLabel = tk.Label(text = "Password for the email: ")
Pass_Entry = tk.Entry(width = 30, show = "*")                               # Entering password and hiding it with **** 
button_password = tk.Button(text = "Log in", command = login)               # Login button 

# The next section appears after login 

Receiver_Label = tk.Label(text = "To who do you want to send the emails to?")   
Receiver_Entry = tk.Entry(width = 30)                                       # Entering receiver email 
Subject_Label = tk.Label(text = "Enter the subject of the email: ")
Subject_Entry = tk.Entry()                                                  # Entering subject of the email 
Content_Label = tk.Label(text = "Enter the message in the email: ") 
Content_Entry = tk.Entry()                                                  # Entering content of the email 
button_launch = tk.Button(text = "Press to send the emails", command = lambda: send_emails(count_entry.get())) 
# Button to send the emails, the command activates send_emails() with the number of emails to send as attribute -> count_entry.get() 

# For spam mode 
spam_mode = -1                                                              # -1 means off 
button_spam = tk.Button(text = "Activate 'spam' mode ", command = activate_spam)                    # Button to activate spam mode 
count_label = tk.Label(text ="How many emails do you want to send? (Must be <=1000)", width = 70)   
count_entry = tk.Entry(width = 3)                                                                   # Entering number of emails to send

# These are packed here because all the other packs are inside functions to make them appear when needed 
sender_email_Label.pack()                                                   
sender_email_Entry.pack()                                                   
PassLabel.pack()
Pass_Entry.pack()
button_password.pack()                      # Packing the sender email, password and login button entries and labels 
root.show_root()                            # Show the window          



