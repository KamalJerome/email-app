import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from tkinter import *
from tkinter import filedialog
import tkinter as tk
from tkinter import ttk
import imaplib
import base64
import os
import email



#=========================================================

def send():
    email_user = e_id.get("1.0",'end-1c')
    email_password = e_password.get("1.0",'end-1c')
    email_send = e_emailsend.get("1.0",'end-1c')
    subject = e_subject.get("1.0",'end-1c')
    cc = e_cc.get("1.0",'end-1c')

    rcpt = cc.split(",")+[email_send]
    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = email_send
    msg['Subject'] = subject
    msg['Cc'] = cc

    body = e_body.get("1.0",'end-1c')
    msg.attach(MIMEText(body,'plain'))

    filename= e_attachment.get("1.0",'end-1c')

    if filename != "":
        attachment= open(filename,'rb')
        part = MIMEBase('application','octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',"attachment; filename= "+filename)
        msg.attach(part)
        text = msg.as_string()
    else:
        text = msg.as_string()
    
    try:
        server = smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login(email_user,email_password)
        server.sendmail(email_user,rcpt,text)
        emailinfo.config(text="Email sent Successfully", fg = "green")
        server.quit()
    except:
        emailinfo.config(text="Email failed", fg = "red")
        
#============================

def reset():
  e_id.delete('1.0','end')
  e_password.delete('1.0','end')
  e_emailsend.delete('1.0','end')
  e_subject.delete('1.0','end')
  e_body.delete('1.0','end')
  e_attachment.delete('1.0','end')
  e_cc.delete('1.0','end')
  emailinfo.config(text="")

#============================ 

def browsefile():
        directory = filedialog.askopenfilename(initialdir = "\\", title = "Select a File", filetypes = (("Text files","*.txt*"),("All files","*.*")))
        filenametext = directory

        e_attachment.insert('end-1c', filenametext)

#============================  

def showinbox():
    window = Toplevel(root)
    window.grab_set()
    window.geometry("1200x700")
    window.title("Inbox")

    inboxicon = PhotoImage(file = 'portphoto.png')
    window.iconphoto(False, inboxicon)

    def update(rows):
        trv.insert('','end',values=rows)
        #print('Inserted',rows[1])

    def getrow(event):
        entfrom.delete('1.0',END)
        entsub.delete('1.0',END)
        entbody.delete('1.0',END)
        entdate.delete('1.0',END)
        entatt.delete('1.0',END)
        rowid = trv.identify_row(event.y)
        selected = trv.focus()
        values = trv.item(selected,'values')
        entfrom.insert('1.0',values[0])
        entsub.insert('1.0',values[1])
        entbody.insert('1.0',values[2])
        entdate.insert('1.0',values[3])
        entatt.insert('1.0',values[4])

    trv = ttk.Treeview(window, columns=(1,2,3,4,5), show="headings", height="10")
    trv.pack()

    trv.bind('<Double-1>', getrow)

    email_user = "etesting865@gmail.com"
    email_pass = "865testing"

    def get_inbox():
        mail = imaplib.IMAP4_SSL("imap.gmail.com",993)
        mail.login(email_user, email_pass)
        mail.select('"Inbox"')

        result, searchdata = mail.search(None, "ALL")
        my_message = []

        for num in searchdata[0].split():
            email_data = {}
            result, data = mail.fetch(num, '(RFC822)')
            result, b = data[0]
            email_message = email.message_from_bytes(b)
            for part in email_message.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True)
                    email_data['body'] = body.decode()
                elif part.get_content_type() == "text/html":
                    html_body = part.get_payload(decode=True)
                    email_data['html_body'] = html_body.decode()
                if part.get_content_maintype() == 'multipart':
                    continue
                if part.get('Content-Disposition') is None:
                    continue
                attname = part.get_filename()
            my_message.append(email_data)
            size = len(email_data['html_body'])
            bod = email_data['html_body'][15:size - 8]
            sub = email_message['subject']
            fro = email_message['from']
            date = email_message['date']
            att = attname
            #print("Data: ",email_data)
            #print("Msg: ",email_message)
            rows = (fro,sub,bod,date,att)
            update(rows)
        rows=()

    def attdwnld():
        email_user = "etesting865@gmail.com"
        email_pass = "865testing"

        mail = imaplib.IMAP4_SSL("imap.gmail.com",993)
        mail.login(email_user, email_pass)
        mail.select()

        type, data = mail.search(None, 'ALL')
        mail_ids = data[0]
        id_list = mail_ids.split()

        for num in data[0].split():
            typ, data = mail.fetch(num, '(RFC822)' )
            raw_email = data[0][1]
        # converts byte literal to string removing b''
            raw_email_string = raw_email.decode('utf-8')
            email_message = email.message_from_string(raw_email_string)
        # downloading attachments
            for part in email_message.walk(): 
                if part.get_content_maintype() == 'multipart':
                    continue
                if part.get('Content-Disposition') is None:
                    continue
                fileName = part.get_filename()
                if bool(fileName):
                    filePath = os.path.join('D:\\Python\\Python Scripts\\EmailApp\\Dwnlds', fileName)
                    if not os.path.isfile(filePath) :
                        fp = open(filePath, 'wb')
                        fp.write(part.get_payload(decode=True))
                        fp.close()
                    subject = str(email_message).split("Subject: ", 1)[1].split("\nTo:", 1)[0]
                    #print('Downloaded "{file}" from email titled "{subject}" with UID {uid}.'.format(file=fileName, subject=subject, uid=num.decode('utf-8')))
                    attinfo.config(text="Downloaded", fg = "green")

    if __name__ == "__main__":
        my_inbox = get_inbox()

    trv.heading(1, text="From")
    trv.column(1, minwidth=0, width=300, stretch=NO)
    trv.heading(2, text="Subject")
    trv.column(2, minwidth=0, width=200, stretch=NO)
    trv.heading(3, text="Body")
    trv.column(3, minwidth=0, width=200, stretch=NO)
    trv.heading(4, text="Date")
    trv.column(4, minwidth=0, width=200, stretch=NO)
    trv.heading(5, text="Attachments")
    trv.column(5, minwidth=0, width=200, stretch=NO)

    trv.bind('<Double-1>', getrow)

    fromlb = Label(window, text="From", font=("bold", 10))
    fromlb.place(x=20, y=250)
    sublb = Label(window,text="Subject",font=("bold", 10))
    sublb.place(x=20,y=300)
    bodylb = Label(window,text="Body",font=("bold", 10))
    bodylb.place(x=20,y=350)
    datelb = Label(window,text="Date",font=("bold", 10))
    datelb.place(x=20,y=600)
    attlb = Label(window,text="Attachments",font=("bold", 10))
    attlb.place(x=20,y=650)

    entfrom = Text(window,height = 1, width = 80)
    entfrom.place(x=150, y=250)
    entsub = Text(window,height = 1, width = 80)
    entsub.place(x=150, y=300)
    entbody = Text(window,height = 14, width = 100)
    entbody.place(x=150, y=350)
    entdate = Text(window,height = 1, width = 80)
    entdate.place(x=150, y=600)
    entatt = Text(window,height = 1, width = 80)
    entatt.place(x=150, y=650)

    inbx = Button(window, text="Download Files", font=("italic", 10), bg="white", command=attdwnld)
    inbx.place(x=800, y=645)
    attinfo = Label(window,text="",font=("bold", 10), fg = "green")
    attinfo.place(x=980,y=647)

root=Tk()
root.geometry("800x500")
root.title("Custom Email App")
icon = PhotoImage(file = 'portphoto.png')
root.iconphoto(False, icon)

id = Label(root, text="Email ID", font=("bold", 10))
id.place(x=20, y=30)

password = Label(root,text="Password",font=("bold", 10))
password.place(x=20,y=60)

emailsend = Label(root,text="Receiver Email ID",font=("bold", 10))
emailsend.place(x=20,y=90)

cc = Label(root,text="CC",font=("bold", 10))
cc.place(x=20,y=120)

subject = Label(root,text="Subject",font=("bold", 10))
subject.place(x=20,y=150)

body = Label(root,text="Body",font=("bold", 10))
body.place(x=20,y=180)

attachment = Label(root,text="Attachment",font=("bold", 10))
attachment.place(x=20,y=420)

emailinfo = Label(root,text="",font=("bold", 10), fg = "green")
emailinfo.place(x=300,y=450)


e_id = Text(height = 1, width = 50)
e_id.place(x=150, y=30)

e_password = Text(height = 1, width = 50)
e_password.place(x=150, y=60)

e_emailsend = Text(height = 1, width = 50)
e_emailsend.place(x=150, y=90)

e_cc = Text(height = 1, width = 50)
e_cc.place(x=150, y=120)

e_subject = Text(height = 1, width = 50)
e_subject.place(x=150, y=150)

e_body = Text(height = 14)
e_body.place(x=150, y=180)

e_attachment= Text(height = 1, width = 50)
e_attachment.place(x=150, y=420)

send = Button(root, text="Send", font=("italic", 10), bg="white", command=send)
send.place(x=20, y=450)

reset = Button(root, text="Reset", font=("italic", 10), bg="white", command=reset)
reset.place(x=100, y=450)

browsebtn = Button(root, text="Browse", font=("italic", 10), bg="white", command=browsefile)
browsebtn.place(x=580, y=415)

inbx = Button(root, text="Show Inbox", font=("italic", 10), bg="white", command=showinbox)
inbx.place(x=180, y=450)

#=========================================================
root.mainloop()