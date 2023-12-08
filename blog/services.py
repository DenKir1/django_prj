from django.conf import settings
from django.core.mail import send_mail



def send_mail_for100(id_):
    send_mail(
        'Блог набрал 100 просмотров!!',
        f'Ваш блог с ID({id_}) набрал просмотры для отправки этого сообщения, поздравляем!',
        settings.EMAIL_HOST_USER,
        ['kird.den@rambler.ru'],
    )
