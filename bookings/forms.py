from django import forms

from .models import Booking, Review


class StyleMixin:
    """Миксин для унификации стилей форм"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_field_styles()

    def set_field_styles(self):
        """Устанавливает общие стили для всех полей формы"""
        for field_name, field in self.fields.items():
            # Базовые классы для всех полей
            field.widget.attrs.update({
                'class': 'form-control',
                'style': 'margin-bottom: 15px;'
            })

            # Особые стили для определенных типов полей
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                    'class': 'form-control input-text',
                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class': 'form-control textarea',
                    'rows': 4,
                })
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({
                    'class': 'form-select',
                })


class BookingForm(StyleMixin, forms.ModelForm):
    """
    Форма для создания и редактирования бронирований с унифицированными стилями
    """
    date = forms.DateField(
        widget=forms.DateInput(
            format='%d-%m-%Y',
            attrs={
                'placeholder': 'дд-мм-гггг',
                'class': 'form-control date-input'
            }
        ),
        input_formats=['%d-%m-%Y'],
        label="Дата бронирования"
    )

    time = forms.TimeField(
        widget=forms.TimeInput(
            format='%H:%M',
            attrs={
                'placeholder': 'ЧЧ:ММ',
                'class': 'form-control time-input'
            }
        ),
        input_formats=['%H:%M'],
        label="Время бронирования"
    )

    class Meta:
        model = Booking
        fields = ['name', 'email', 'phone', 'date', 'time', 'guests']
        labels = {
            'name': 'Имя',
            'email': 'Электронная почта',
            'phone': 'Телефон',
            'guests': 'Количество гостей',
        }
        help_texts = {
            'date': 'Формат: дд-мм-гггг (например, 05-08-2025)',
            'time': 'Формат: ЧЧ:ММ (например, 18:00)',
        }
        widgets = {
            'phone': forms.TextInput(attrs={
                'placeholder': '+7 (XXX) XXX-XX-XX',
                'pattern': '\+7\s?[\(]{0,1}\d{3}[\)]{0,1}\s?\d{3}[-]{0,1}\d{2}[-]{0,1}\d{2}'
            }),
        }


class ReviewForm(StyleMixin, forms.ModelForm):
    """
    Форма для отправки отзывов с унифицированными стилями
    """

    class Meta:
        model = Review
        fields = ['name', 'email', 'comment', 'rating']
        labels = {
            'name': 'Ваше имя',
            'email': 'Электронная почта',
            'comment': 'Комментарий',
            'rating': 'Оценка (1-5)'
        }
        widgets = {
            'comment': forms.Textarea(attrs={
                'placeholder': 'Оставьте ваш отзыв...',
                'class': 'form-control textarea'
            }),
            'rating': forms.NumberInput(attrs={
                'min': 1,
                'max': 5,
                'class': 'form-control rating-input'
            }),
        }
