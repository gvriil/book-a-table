from django.db import models


class Booking(models.Model):
    """
    Модель для хранения информации о бронированиях.

    Атрибуты:
        name (str): Имя клиента.
        email (str): Электронная почта клиента.
        phone (str): Номер телефона клиента.
        date (date): Дата бронирования.
        time (time): Время бронирования.
        guests (int): Количество гостей.
    """
    name = models.CharField(
        max_length=100,
        verbose_name="Имя клиента"
    )
    email = models.EmailField(
        verbose_name="Электронная почта клиента"
    )
    phone = models.CharField(
        max_length=15,
        verbose_name="Номер телефона клиента"
    )
    date = models.DateField(
        verbose_name="Дата бронирования"
    )
    time = models.TimeField(
        verbose_name="Время бронирования"
    )
    guests = models.PositiveIntegerField(
        verbose_name="Количество гостей"
    )

    def __str__(self):
        """
        Возвращает строковое представление бронирования.

        Пример: "Имя клиента - YYYY-MM-DD в HH:MM"
        """
        return f"{self.name} - {self.date} в {self.time}"


class Review(models.Model):
    """
    Модель для хранения отзывов.

    Атрибуты:
        name (str): Имя автора отзыва.
        email (str): Электронная почта автора.
        comment (str): Текст отзыва.
        rating (int): Оценка из 5.
        approved (bool): Одобрен ли отзыв для публикации.
        created_at (datetime): Дата и время создания отзыва.
    """
    name = models.CharField(
        max_length=200,
        verbose_name="Имя автора"
    )
    email = models.EmailField(
        verbose_name="Электронная почта автора"
    )
    comment = models.TextField(
        verbose_name="Текст отзыва"
    )
    rating = models.PositiveIntegerField(
        default=5,
        verbose_name="Оценка",
        help_text="Из 5"
    )
    approved = models.BooleanField(
        default=False,
        verbose_name="Одобрен для публикации"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )

    def __str__(self):
        """
        Возвращает строковое представление отзыва.

        Пример: "Отзыв от Имя (Approved)/(Pending)"
        """
        status = "Одобрен" if self.approved else "Под ожиданием"
        return f"Отзыв от {self.name} ({status})"
