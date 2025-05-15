from django.contrib import admin
from django.urls import include
from django.urls import path
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter

from bookings.views import BookingViewSet
from bookings.views import (
    book_table,
    booking_success,
    booking_list,
    weekly_calendar,
    available_timeslots,
    home,
    review_ticker,
    submit_review,
    update_booking_lookup,
    cancel_lookup,
    confirm_cancel,
    cancel_booking,
    update_booking
)

# Имя пространства имён для приложения 'bookings'
app_name = 'bookings'
router = DefaultRouter()
router.register(r'bookings', BookingViewSet)

# Пути, связанные с бронированием
booking_patterns = [

    path('book/', book_table, name='book_table'),  # Страница для бронирования
    path('success/', booking_success, name='booking_success'),  # Успешное бронирование
    path('success/<int:booking_id>/', booking_success, name='booking_success'),
    # По ID бронирования
    path('bookings/', booking_list, name='booking_list'),  # Список всех бронирований
    path('update/<int:booking_id>/', update_booking, name='update_booking'),
    # Обновление бронирования
    path('cancel/<int:booking_id>/', cancel_booking, name='cancel_booking'),  # Отмена бронирования
    path('cancel-lookup/', cancel_lookup, name='cancel_lookup'),  # Поиск для отмены бронирования
    path('confirm-cancel/<int:booking_id>/', confirm_cancel, name='confirm_cancel'),
    # Подтверждение отмены
    path('update-lookup/', update_booking_lookup, name='update_booking_lookup'),
    # Поиск для обновления бронирования
]

# Пути, связанные с отзывами
review_patterns = [
    path('submit-review/', submit_review, name='submit_review'),  # Отправка отзыва
    path('review-ticker/', review_ticker, name='review_ticker'),  # Лента отзывов
]

# Статические страницы (например, меню ресторана)
menu_patterns = [
    path(
        'lunch-menu/',
        TemplateView.as_view(template_name="bookings/lunch_menu.html"),
        name='lunch_menu'
    ),  # Страница с обедом
    path(
        'dinner-menu/',
        TemplateView.as_view(template_name="bookings/dinner_menu.html"),
        name='dinner_menu'
    ),  # Страница с ужином
]

# Основные пути (маршруты) приложения
urlpatterns = [
                  path('api/', include(router.urls)),
                  path('admin/', admin.site.urls),  # Админка Django
                  path('', home, name='home'),  # Главная страница сайта
                  path('timeslots/', available_timeslots, name='available_timeslots'),
                  # Доступные слоты бронирования
                  path('weekly-calendar/', weekly_calendar, name='weekly_calendar'),
                  # Недельный календарь бронирования
              ] + booking_patterns + review_patterns + menu_patterns  # Добавляем маршруты из других категорий
