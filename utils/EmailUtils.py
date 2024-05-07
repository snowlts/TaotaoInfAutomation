import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from email.mime.multipart import MIMEMultipart
from email.header import Header

from config.config import config



class Email:
    def __init__(self, sender=config.email['sender'], recievers=config.email['recievers'],
                 smtp_server=config.email['smtp_server'], username=config.email['username'],
                 password=config.email['password']):
        self.sender = sender
        self.recievers = recievers
        self.username = username
        self.password = password
        self.smtp_server = smtp_server

    def send(self,subject,mail_text,attachment=None):
        mail_msg = """
        <p>测试报告链接：</p>
        <p><a href="{}">请点击</a></p>
        """.format(mail_text)
        msg = MIMEMultipart()
        msg['From'] = Header(self.sender,'utf-8')  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        # msg['To'] = self.recievers # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['To'] = Header(','.join(self.recievers),'utf-8')  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = Header(subject,'utf-8')  # 邮件的主题，也可以说是标题

        msg.attach(MIMEText(mail_msg, 'html', 'utf-8'))

        # 添加附件
        if attachment:
            att1 = MIMEText(open(attachment, 'rb').read(), 'base64', 'utf-8')
            att1["Content-Type"] = 'application/octet-stream'
            # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
            att1["Content-Disposition"] = 'attachment; filename="%s"' % attachment
            msg.attach(att1)
        try:
            server = smtplib.SMTP_SSL(self.smtp_server, 465)  # 发件人邮箱中的SMTP服务器，端口是25
            server.login(self.sender, self.password)  # 括号中对应的是发件人邮箱账号、邮箱密码
            server.sendmail(self.sender, self.recievers, msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
            server.quit()  # 关闭连接
        except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
            raise


mail = Email()
# mail.send('hi','https://www.baidu.com')

