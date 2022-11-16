# # import smtplib
# # import sendgrid
# # import os
# # from sendgrid.helpers.mail import Mail, Email, To, Content,sg
# # import os
# # from sendgrid import SendGridAPIClient
# # from sendgrid.helpers.mail import *
# # email_list=['jayaprakash291029@gmail.com']
# # message = Mail(
# #         from_email='jayaprakash.p.2019.cse@rajalakshmi.edu.in',
# #         to_emails= email_list,
# #         subject='Sending with Twilio SendGrid is Fun',
# #         html_content="hi test")
# # try:
# #         sg = SendGridAPIClient(apikey="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")
# #         response = sg.send(message)
# #         print(response.status_code)
# #         print(response.body)
# #         print(response.headers)
# # except Exception as e:
# #         print(e.message)
# # SUBJECT = "expense tracker"
# # s = smtplib.SMTP('smtp.gmail.com', 587)

# # def sendmail(TEXT,email):
# #     print("sorry we cant process your candidature")
# #     s = smtplib.SMTP('smtp.gmail.com', 587)
# #     s.starttls()
# #     s.login("il.jayaprakash291029@gmail.com", "ROOT")
# #     message  = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
# #     s.sendmail("il.jayaprakash291029@gmail.com", email, message)
# #     s.quit()
# # def sendgridmail(user,TEXT):
  
# #     from_email = Email("jayaprakash291029@gmail.com") 
# #     to_email = To(user) 
# #     subject = "Sending with SendGrid is Fun"
# #     content = Content("text/plain",TEXT)
# #     mail = Mail(from_email, to_email, subject, content)

# #     # Get a JSON-ready representation of the Mail object
# #     mail_json = mail.get()
# #     # Send an HTTP POST request to /mail/send
# #     response = sg.client.mail.send.post(request_body=mail_json)
# #     print(response.status_code)
# #     print(response.headers)
# # import os
# # import sendgrid
# # from sendgrid import SendGridAPIClient
# # from sendgrid.helpers.mail import  Mail, Email, To, Content,sg

# # sg = sendgrid.SendGridAPIClient(api_key='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')
# # from_email = Email("jayaprakash691029@gmail.com")
# # to_email = To("jayaprakash691029@gmail.com")
# # subject = "Sending with SendGrid is Fun"
# # content = Content("text/plain", "and easy to do anywhere, even with Python")
# # mail = Mail(from_email, to_email, subject, content)
# # response = sg.client.mail.send.post(request_body=mail.get())
# # print(response.status_code)
# # print(response.body)
# # print(response.headers)
# # import sendgrid
# from sendgrid import SendGridAPIClient
# from sendgrid.helpers.mail import Mail
# mes=Mail(from_email='jayaprakash291029@gmail.com',
#          to_emails='jayaprakash.p.2019.cse@rajalakshmi.edu.in',
#          subject='just testing ',
#          html_content='this is my mail')
# sg=SendGridAPIClient("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")
# response=sg.send(mes)
# print(response.status_code,response.body)

from flask import Flask
from flask_mail import Mail, Message

sender_email="jayaprakash291029@gmail.com"
        rec_email= session['username']
        password='xtbrhwpqbdbxyjir'
        message='ALERT MESSAGE FROM EXPENSE TRACKER !PLEASE CHECK  YOUR DAILY EXPENSE YOUR DAILY EXPENSE IS CROSS YOUR MONTHLY LIMIT. UPDATE YOUR MONTHLY LIMIT AND AVOID YOUR UNWANTED DAILY EXPENSE'
        # soup=BeautifulSoup(html_data,'html.parser')      
        print(message)
        server=smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login(sender_email,password)
        print("login successfully")
        server.sendmail(sender_email,rec_email,message)
        print("emaail has been sende successfully")