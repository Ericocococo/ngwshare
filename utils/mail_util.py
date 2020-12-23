import smtplib
from email.mime.text import MIMEText
from email.header import Header
import traceback

def send_mail(to_addr=None,header=None,content=None):
    # # 发信人
    # from_addr = '969282488@qq.com'
    # token = 'kpofdicliftibfcc'

    # 发信人
    from_addr = '296348304@qq.com'
    token = 'jrhflcppohwsbjfj'

    # 收信方邮箱
    # to_addr = '296348304@qq.com'
    # to_addr = 'wj296348304@163.com'

    # 发信服务器
    smtp_server = 'smtp.qq.com'
    try:
        # 邮箱正文内容，第一个参数为内容，第二个参数为格式(plain 为纯文本)，第三个参数为编码
        msg = MIMEText(content, 'plain', 'utf-8')
        # 邮件头信息
        msg['From'] = Header(from_addr)
        msg['To'] = Header(to_addr)
        msg['Subject'] = Header(header)

        server = smtplib.SMTP_SSL(smtp_server)
        server.connect(smtp_server, 465)
        server.login(from_addr, token)
        server.sendmail(from_addr, to_addr, msg.as_string())
        server.quit()
        return True
    except:
        print(traceback.format_exc())
        return False

if __name__ == '__main__':
    to_mail = 'wj296348304@163.com'
    mail_header = '【数据产品】【龙虎榜】'
    mail_content = '[信息]数据保存成功！！！'
    mail_flag = send_mail(to_mail,mail_header,mail_content)
    print(mail_flag)


