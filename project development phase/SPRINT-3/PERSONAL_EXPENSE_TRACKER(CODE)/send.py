

from flask import Flask
from flask_mail import Mail, Message

sender_email="jayaprakash@gmail.com"
        rec_email= session['username']
        password='xxxxxxxxxxxxxxxxx'
        message='ALERT MESSAGE FROM EXPENSE TRACKER !PLEASE CHECK  YOUR DAILY EXPENSE YOUR DAILY EXPENSE IS CROSS YOUR MONTHLY LIMIT. UPDATE YOUR MONTHLY LIMIT AND AVOID YOUR UNWANTED DAILY EXPENSE'
        # soup=BeautifulSoup(html_data,'html.parser')      
        print(message)
        server=smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login(sender_email,password)
        print("login successfully")
        server.sendmail(sender_email,rec_email,message)
        print("emaail has been sende successfully")