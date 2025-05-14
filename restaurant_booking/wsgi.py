"""
WSGI конфигурация для проекта restaurant_booking.

Этот файл предоставляет WSGI callable объект на уровне модуля с именем ``application``.
Он используется для развертывания приложения, выполняя взаимодействие
между сервером WSGI и Django-приложением.

Для получения дополнительной информации о данном файле см. документацию:
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Устанавливаем модуль настроек проекта по умолчанию
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurant_booking.settings')

# Создаём объект WSGI приложения
application = get_wsgi_application()
