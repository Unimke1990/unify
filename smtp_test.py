import smtplib

def test_smtp_connection():
    smtp_server = "smtp.gmail.com"
    smtp_ports = [587, 465, 25]  # List of ports to try
    smtp_username = "agimagba1990@gmail.com"
    smtp_password = "mhea jfpl hzvd vtwn"

    for smtp_port in smtp_ports:
        try:
            if smtp_port == 465:
                server = smtplib.SMTP_SSL(smtp_server, smtp_port)
            else:
                server = smtplib.SMTP(smtp_server, smtp_port)
                server.starttls()
            server.login(smtp_username, smtp_password)
            print(f"SMTP connection successful on port {smtp_port}")
            server.quit()
            return
        except Exception as e:
            print(f"SMTP connection failed on port {smtp_port}: {e}")

if __name__ == "__main__":
    test_smtp_connection()