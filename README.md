# EmailSender

Simple email sender using tkinter for the GUI. 

The main tkinter window is created from the TkinterWindow class to save space. Labels and entries are explicitly created and packed. 

Supports Gmail, Outlook, Hotmail, Yahoo, AT&T, Comcast and Verizon. User needs to allow "less secure app access" in account settings if necessary. 

Take into consideration that this is only for demonstration purposes.

## Simple user guide 

    1) Input your login credentials and press "Log in". 
    2) Then, input (in order), the email address of the person that will receive the emails, the subject of the email and the text in the email. 
    3) If you wish to enter the "multiple emails" mode, press the button on the right. 
       If you pressed the button by accident, you can press it again to go back to "one email mode". 
       
       When in "multiple emails" mode, you can choose the amount of emails to send, please choose a natural number between 1 and 1000, inclusively. 
        To avoid getting limited by email services, the emails will be sent at a 0.6s interval and the program will pause for 1min every 50 emails. 
        The email count and sleep status will be sent to the terminal that you're using. 
        The emails sent in this mode will all have the number of the email added next to the Subject to avoid them being all merged into one in the inbox.
        *Take into consideration that the window might freeze in spam mode, don't worry tough, the messages will continue being sent.* 

    4) When you are ready, press the button on the left to send the emails/email. 



