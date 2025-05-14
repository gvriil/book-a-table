"""
ASGI конфигурация для проекта restaurant_booking.

Этот файл предоставляет ASGI callable объект на уровне модуля с именем ``application``.
Он используется для асинхронного развертывания приложения.

Для получения дополнительной информации о данном файле см. документацию:
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

# Устанавливаем модуль настроек проекта по умолчанию
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurant_booking.settings')

# Создаём объект ASGI приложения
application = get_asgi_application()