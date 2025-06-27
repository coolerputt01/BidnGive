from django.core.mail import send_mail
from django.conf import settings

def send_otp_email(user_email, otp):
    subject = 'Your BID "N" GIVE Email Verification OTP'
    message = f'Hello,\n\nYour OTP for email verification is: {otp}\n\nThank you for using BID "N" GIVE.'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]
    
    send_mail(subject, message, from_email, recipient_list)
