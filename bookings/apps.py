from django.apps import AppConfig


class BookingsConfig(AppConfig):
    """
    Конфигурация приложения 'bookings'.

    Это приложение отвечает за управление бронированиями, отзывами и связанным функционалом.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bookings'
