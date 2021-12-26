import smtplib 
import tkinter as tk
import assets 
from time import sleep 
from json import load 

with open("colors.json", "r") as j_file:                
    colors = load(j_file) # JSON is not really necessary for this application but I wanted to practice using it 

def login(s_email_entry, s_email_label, pass_entry, pass_label): 
    global connect                                            # connect is global because its a unique obj that will need to be referenced later
    s_email = s_email_entry.get().strip()                                       # Getting sender email 

    (smtp_server, port) = assets.get_provider(s_email)                          # Getting the provider and the appropiate port

    if (smtp_server, port) == (None, None):                                     # if nothing is returned, get_provider() didn't find a supported email
        s_email_label.configure(text = "Sorry that email provider is not supported")                 
    else: 
        connect = smtplib.SMTP(smtp_server, port)                               # setting up connection 
        connect.ehlo()                                                          # starting connection
        connect.starttls()                                                      # starting encryption before login
        try:                                                                    # First attempting log in 
            key = pass_entry.get()                                              # Getting password 
            connect.login(s_email, key)                                         # Logging in 
            
        except smtplib.SMTPAuthenticationError:                                 # If the password is incorrect 
            s_email_label.configure(text = "Wrong password, try again", bg = colors["login_failure"]["sender_email_Label"])
            pass_label.configure(bg = colors["login_failure"]["PassLabel"])
            pass_entry.delete(0, 'end')                                         # Clear the entry 
        
        else:                                                                   # If log in was successful 
            s_email_label.configure(text = "Logged in!", bg = colors["login_success"]["sender_email_Label"])  
            pass_label.configure(bg = colors["login_success"]["PassLabel"])                           
            button_password.configure(state = tk.DISABLED)                      # Disable button to log in 

            root.resize_root("591x399")
            assets.pack_widgets(widgets_after_login)
            button_launch.pack(side = tk.LEFT)                                  # Let the message creation entries appear 
            button_multiple_email.pack(side = tk.RIGHT)                                   # Let the 'multiple_email mode' button appear 


def send_emails(q, s_email_entry):    
    s_email = s_email_entry.get().strip()                                                         
    receiver_email = Receiver_Entry.get().strip()                               # Getting receiver email 
    if q == "": q = 1                                              # if there's multiple_email mode is off, q will be "" so just set to 1 to send 1 email 
    try:
        q = int(float(q))                                                       # If float is inputed, convert to int 
    except ValueError:                                                      
        count_label.configure(text ="Email count must be an integer!")          # If str is inputed ValueError will be raised 
    else:
        if q>1000 or q<=0:                                                      # If person inputed too large number or a negative number
            count_label.configure(text ="Email count must be between 0 and 1000!")
        else: 
            if multiple_mode == 1:                                                  # If the multiple_email mode is on 
                count_label.configure(text ="Emails are being sent!")           
                for n in range(1, q+1):                                         # Send the multiple emails
                    message = assets.Email_msg(Subject_Entry.get()+str(n),\
                        Content_Entry.get("1.0", tk.END)).get_msg()                          # Add a number to the title to prevent email merging emails in one
                    connect.sendmail(s_email, receiver_email, message)          # Send the mail 
                    assets.multiple_clock(n)                                        # Run the clock to avoid blocking from provider 

            elif multiple_mode == -1:                                                                          #If multiple_email mode is off 
                message = assets.Email_msg(Subject_Entry.get(), Content_Entry.get("1.0", tk.END)).get_msg()             # Getting message (without number this time)
                connect.sendmail(s_email, receiver_email, message)                                         # Send email 
                print("Email sent!")

            else: 
                print("Error, multiple mode not in {-1, 1}")
            sleep(1)
            connect.quit()                                                  # Disconnect from service 
            root.destroy_root()                                             # Destroy window and close program 



# For multiple emails mode
def activate_multiple(label1, entry1, label2, button1):                    # Turning multiple_email mode on and off
    global multiple_mode                                                  # Global to keep track of the multiple_email mode 'status'  
    multiple_mode = multiple_mode*-1                                               
    if multiple_mode == 1:  
        root.color_root(colors["multiple_on"]["background_color"])                                                    
        label1.pack()                                                   
        entry1.pack()                                                  # Make the multiple_email mode settings appear when on 
        label2.pack(side = tk.LEFT, anchor = tk.SW, ipady = 7) 
        button1.pack(side = tk.RIGHT, anchor = tk.SE, ipady = 7)
    else: 
        root.color_root(colors["multiple_off"]["background_color"])
        label1.pack_forget()
        entry1.pack_forget()                                           # Remove the settings if multiple_email mode is off 
        label2.pack_forget() 
        button1.pack_forget()

def get_estimate(entry, label): 
    q = entry.get() 
    if q == "": q = 1                                                           # if there's multiple_email mode is off, q will be "" so just set to 1 to send 1 email
    try:
        q = int(float(q))                                                       # If float is inputed, convert to int 
    except ValueError:                                                      
        count_label.configure(text ="Email count must be an integer!")          # If str is inputed ValueError will be raised 
    else:
        if q>1000 or q<=0:                                                      # If person inputed too large number or a negative number
            count_label.configure(text ="Email count must be between 0 and 1000!")
        else: 
            qtt_sleeps = int(q/50) * 60
            total_time = int(qtt_sleeps + ((q-1)*0.6))
            label.configure(text = f"Estimated time in sec: {total_time}")

if __name__ == "__main__":  # Not putting this in a main() function because vars here are referenced by other functions 
    root = assets.TkinterWindow('main', 'Email sender', '229x134')              # Setting up window settings 
    root.construct_root()                                                       # Creating window 

    sender_email_Label = tk.Label(text = "Your email address: ")                
    PassLabel = tk.Label(text = "Password for the email: ")

    sender_email_Entry = tk.Entry(width = 30)                                   # Entering sender email
    Pass_Entry = tk.Entry(width = 30, show = "*")                               # Entering password and hiding it with **** 

    button_password = tk.Button(text = "Log in", command = lambda: login(sender_email_Entry, sender_email_Label, Pass_Entry, PassLabel))     

    widgets_login = [sender_email_Label, sender_email_Entry, PassLabel, Pass_Entry, button_password] # List of the widgets that are needed for login 

    # The next section appears after login 

    Receiver_Label = tk.Label(text = "To who do you want to send the emails to?")   
    Subject_Label = tk.Label(text = "Enter the subject of the email: ")
    Content_Label = tk.Label(text = "Enter the message in the email: ") 

    Receiver_Entry = tk.Entry(width = 30)                                       # Entering receiver email 
    Subject_Entry = tk.Entry()                                                  # Entering subject of the email 
    Content_Entry = tk.Text(height = 5, width = 30) 
                                                    # Entering content of the email 
    button_launch = tk.Button(text = "Press to send the emails", command = lambda: send_emails(count_entry.get(), sender_email_Entry)) 

    widgets_after_login = [Receiver_Label, Receiver_Entry, Subject_Label, Subject_Entry, Content_Label, Content_Entry] 
    # Button to send the emails, the command activates send_emails() with the number of emails to send as attribute -> count_entry.get()   
    multiple_mode = -1                                                              # -1 means off 
    button_multiple_email = tk.Button(text = "Activate 'multiple emails' mode ", command = lambda: activate_multiple(count_label, count_entry, time_est, estimate_time))
    count_label = tk.Label(text ="How many emails do you want to send? (Must be <=1000)", width = 150)   
    count_entry = tk.Entry(width = 5)                                                                   # Entering number of emails to send
    time_est = tk.Label(text = "Estimated time in sec: ") 
    estimate_time = tk.Button(text = "Press to get estimate", command = lambda: get_estimate(count_entry, time_est))

    # These are packed here because all the other packs are inside functions to make them appear when needed 
    assets.pack_widgets(widgets_login)                      # Packing the sender email, password and login button entries and labels    
    root.show_root()  