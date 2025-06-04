# SplitForUS-backend/utils.py

import os
import random
import string

# ----------------------------
# 1) E-posta Gönderme (Örnek: smtplib ile)
# ----------------------------
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(to_address: str, subject: str, body: str) -> None:
    """
    Basit bir SMTP ile e-posta gönderme fonksiyonu.
    Ortam değişkenlerinden SMTP ayarları alınıyor.
    """
    SMTP_SERVER   = os.getenv("SMTP_SERVER", "")
    SMTP_PORT     = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER     = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
    FROM_ADDRESS  = os.getenv("FROM_EMAIL", SMTP_USER)

    if not all([SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASSWORD]):
        raise Exception("E-posta için SMTP ayarları eksik. Lütfen ortam değişkenlerini kontrol edin.")

    message = MIMEMultipart()
    message["From"] = FROM_ADDRESS
    message["To"] = to_address
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(SMTP_USER, SMTP_PASSWORD)
    server.sendmail(FROM_ADDRESS, to_address, message.as_string())
    server.quit()

# ----------------------------
# 2) Doğrulama Kodu Üretme
# ----------------------------
def generate_verification_code(length: int = 6) -> str:
    """
    Rastgele sayısal doğrulama kodu üretir (varsayılan 6 haneli).
    Sadece rakamlardan oluşur.
    """
    return "".join(random.choices(string.digits, k=length))
