# -*- coding: utf-8 -*-
"""mail.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1zQv_3-ayrJPo0PpxsvdxPs6OnTfdqYgA
"""

# -*- coding: utf-8 -*-
import smtplib
from email.mime.text import MIMEText
import ssl
# smtp = ('stn.nagaokaut.ac.jp', 465)
# login = ('s183***', '*****')
# msg = MIMEText('本文')
# msg['Subject'] = '件名'
# msg['From'] = 'twakai@stn.nagaokaut.ac.jp'
# msg['To'] = 'twoamkoai@gmail.com'
class mail:
    def __init__(self, smtp, login):
        self.smtp_server, self.port  = smtp
        self.user, self.pw = login

    def Send(self, msg):
        server = smtplib.SMTP_SSL(self.smtp_server, self.port)
        server.login(self.user, self.pw)
        server.sendmail(msg['From'], [msg['To']], msg.as_string())
        server.quit()