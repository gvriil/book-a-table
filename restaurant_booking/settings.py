"""
Настройки Django для проекта restaurant_booking.

Сгенерировано с помощью команды 'django-admin startproject' для версии Django 4.2.18.

Для получения дополнительной информации по этому файлу:
https://docs.djangoproject.com/en/4.2/topics/settings/

Для полного списка настроек и их описания:
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from pathlib import Path

# Построение путей внутри проекта, как BASE_DIR / 'подкаталог'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Настройки быстрого старта — не подходят для производства
# Подробнее: https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# ВНИМАНИЕ: держите секретный ключ в секрете для работы в режиме производства!
SECRET_KEY = 'django-insecure-=4iva176%d&pw8y#9xms2xcw=m*x+g3@b)%5!6^l3%z%v6_7&6'

# ВНИМАНИЕ: никогда не используйте Debug в режиме производства!
DEBUG = True

# Хосты, разрешённые для работы с приложением
ALLOWED_HOSTS = []

# Определение приложений

INSTALLED_APPS = [
    'django.contrib.admin',  # Управление администрацией
    'django.contrib.auth',  # Аутентификация пользователей
    'django.contrib.contenttypes',  # Управление типами контента
    'django.contrib.sessions',  # Управление сессиями пользователей
    'django.contrib.messages',  # Сообщения для пользователей
    'django.contrib.staticfiles',  # Управление статическими файлами
    'bookings',  # Приложение для работы с бронированием
    'rest_framework',
    'django_extensions',  # Доп. инструменты для разработки (django-extensions)
]

# Промежуточное ПО (Middleware)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # Безопасность
    'django.contrib.sessions.middleware.SessionMiddleware',  # Обработка сессий
    'django.middleware.common.CommonMiddleware',  # Общее промежуточное ПО
    'django.middleware.csrf.CsrfViewMiddleware',  # Защита от CSRF-атак
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Аутентификация
    'django.contrib.messages.middleware.MessageMiddleware',  # Сообщения
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Защита от атак Clickjacking
]

# Основной URL конфигурации
ROOT_URLCONF = 'restaurant_booking.urls'

# Настройки шаблонов

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # Использовать папки для пользовательских шаблонов? (пока пусто)
        'APP_DIRS': True,  # Включить поиск шаблонов в приложениях
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',  # Отладка
                'django.template.context_processors.request',  # Объект запроса
                'django.contrib.auth.context_processors.auth',  # Обработчик аутентификации
                'django.contrib.messages.context_processors.messages',  # Обработчик сообщений
            ],
        },
    },
]

# WSGI-приложение
WSGI_APPLICATION = 'restaurant_booking.wsgi.application'

# База данных
# Поддержка PostgreSQL
# Подробнее: https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # Движок базы данных
        'NAME': os.environ.get('DB_NAME', 'book_a_table'),  # Имя базы данных
        'USER': os.environ.get('DB_USER'),  # Имя пользователя
        'PASSWORD': os.environ.get('DB_PASSWORD', 'book'),  # Пароль (по умолчанию "book")
        'HOST': os.environ.get('DB_HOST', 'db'),  # Адрес хоста
        'PORT': os.environ.get('DB_PORT', default='5432'),  # Порт
    }
}

# Валидация паролей
# Подробнее: https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Интернационализация
# Подробнее: https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'  # Язык ("en-us" — английский)

TIME_ZONE = 'UTC'  # Часовой пояс

USE_I18N = True  # Использовать интернационализацию

USE_TZ = True  # Включить поддержку временных зон

# Статические файлы (CSS, JavaScript, Изображения)
# Подробнее: https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'  # URL-адрес для статических файлов

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),  # Папка со статическими файлами
]

# Основной тип ключей для моделей
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Настройка электронной почты (для отладки)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # Вывод в консоль
EMAIL_HOST = 'localhost'  # Хост для SMTP-сервера
EMAIL_PORT = 1025  # Порт

# Django REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
}
