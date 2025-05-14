from django import forms

from .models import Booking, Review


class BookingForm(forms.ModelForm):
    """
    Форма для создания и редактирования бронирований.

    Поля даты и времени переопределены, чтобы задать пользовательские форматы ввода
    и placeholder для удобства работы клиента.
    """
    date = forms.DateField(
        widget=forms.DateInput(
            format='%d-%m-%Y',
            attrs={
                'placeholder': 'дд-мм-гггг',  # Пример: 05-08-2025
                'type': 'text'  # Используем текст, чтобы placeholder отображался
            }
        ),
        input_formats=['%d-%m-%Y'],
        label="Дата бронирования"
    )
    time = forms.TimeField(
        widget=forms.TimeInput(
            format='%H:%M',
            attrs={
                'placeholder': 'ЧЧ:ММ',  # Пример: 18:00
                'type': 'text'  # Используем текст, чтобы placeholder был видимым
            }
        ),
        input_formats=['%H:%M'],
        label="Время бронирования"
    )

    class Meta:
        """
        Класс Meta задаёт связь формы с моделью Booking.
        Указывает поля формы и дополнительные инструкции по их отображению.
        """
        model = Booking
        fields = ['name', 'email', 'phone', 'date', 'time', 'guests']
        help_texts = {
            'date': 'Введите дату бронирования в формате дд-мм-гггг (например, 05-08-2025).',
            'time': 'Введите время бронирования в формате ЧЧ:ММ (например, 18:00).',
        }
        labels = {
            'name': 'Имя',
            'email': 'Электронная почта',
            'phone': 'Телефон',
            'guests': 'Количество гостей',
        }


class ReviewForm(forms.ModelForm):
    """
    Форма для отправки отзывов пользователей.

    Поддерживает ввод имени, электронной почты, текста отзыва и оценки (по умолчанию до 5).
    Поле "Комментарий" отображается в виде текстовой области (textarea) для удобства ввода.
    Поле "Оценка" ограничено диапазоном значений от 1 до 5.
    """

    class Meta:
        """
        Класс Meta задаёт связь формы с моделью Review.
        Указывает поля формы и их пользовательские виджеты.
        """
        model = Review
        fields = ['name', 'email', 'comment', 'rating']
        widgets = {
            'comment': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Оставьте ваш отзыв...',  # Placeholder для поля комментария
                'class': 'form-textarea'  # Дополнительно можно задать класс CSS
            }),
            'rating': forms.NumberInput(attrs={
                'min': 1,
                'max': 5,
                'placeholder': 'Оценка (от 1 до 5)',  # Placeholder для поля оценки
                'class': 'form-input-number'  # Дополнительно можно задать класс CSS
            }),
        }
        labels = {
            'name': 'Ваше имя',
            'email': 'Электронная почта',
            'comment': 'Комментарий',
            'rating': 'Оценка'
        }
        help_texts = {
            'rating': 'Введите оценку от 1 до 5 (например, 4).'
        }
