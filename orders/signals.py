from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from orders.models import Order
from robots.models import Robot


@receiver(post_save, sender=Robot)
def notify_customer(sender, instance, created, **kwargs):
    """
    Отправка сообщений на почту для тех, кто ждёт заказ.
    """

    if created:
        orders = Order.objects.filter(robot_serial=instance.serial)

        for order in orders:
            model = instance.model
            version = instance.version
            subject = 'Робот в наличии'
            message = (
                f'Добрый день!\n'
                f'Недавно вы интересовались нашим роботом модели {model}, '
                f'версии {version}.\n'
                f'Этот робот теперь в наличии. Если вам подходит этот '
                f'вариант - пожалуйста, свяжитесь с нами.'
            )
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [order.customer.email]

            send_mail(subject, message, from_email, recipient_list)

        orders.delete()
