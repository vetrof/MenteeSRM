import time
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.contrib.auth.models import User
from.models import SpamForAllUsers
from django.core.mail import send_mail


def mail_me_new_contact():
    ...


def mail_all_register_user(spam_id):

    users = User.objects.all()
    text = SpamForAllUsers.objects.get(id=spam_id)
    message = text.message

    recipient_list = []
    for user in users:
        if user.email:
            user_email = user.email
            recipient_list.append(user_email)

    for mail in recipient_list:
        mailto = []
        mailto.append(mail)

        # Получите HTML-шаблон
        html_template = get_template('email_template.html')
        html_content = html_template.render({'username': 'user_name', 'text': message})

        # Отправьте HTML-письмо
        subject = text.subject
        from_email = 'admin@django.help'

        msg = EmailMultiAlternatives(subject=subject, body="", from_email=from_email, to=mailto)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        print(mailto)









