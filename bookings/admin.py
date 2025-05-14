from django.contrib import admin
from .models import Booking, Review

# Регистрация модели Booking в интерфейсе администратора
admin.site.register(Booking)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """
    Класс интерфейса администратора для управления объектами Review.

    Настраивает отображение, фильтрацию, поиск и действия
    для отзыва в панели администратора Django.
    Также предоставляет действие для быстрого утверждения выбранных отзывов.
    """
    list_display = ('name', 'email', 'approved', 'created_at')  # Поля для отображения
    list_filter = ('approved', 'created_at')  # Фильтры в боковой панели
    search_fields = ('name', 'email', 'comment')  # Поля для поиска
    actions = ['approve_reviews']  # Действия для админки

    def approve_reviews(self, request, queryset):
        """
        Пользовательское действие для утверждения выбранных отзывов.

        Аргументы:
            request: Текущий объект HttpRequest.
            queryset: QuerySet из выбранных объектов Review, которые нужно утвердить.
        """
        queryset.update(approved=True)
        self.message_user(request, "Выбранные отзывы были успешно утверждены.")

    approve_reviews.short_description = "Утвердить выбранные отзывы"