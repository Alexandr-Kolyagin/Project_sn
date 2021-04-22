import smtplib

def email_password_forgot(old_email,new_password):
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    addr_from = "mail_intre_change@mail.ru"
    addr_to = old_email
    password = "C30a558ef7"

    msg = MIMEMultipart()
    msg['From'] = addr_from
    msg['To'] = addr_to
    msg['Subject'] = 'Восстановление пароля'

    body = f"Ваш новый пароль '{new_password}'"
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.mail.ru', 587)
    server.set_debuglevel(
    True)
    server.starttls()
    server.login(addr_from, password)
    server.send_message(msg)
    server.quit()
