"""
Этот файл содержит функции представления (views) для приложения bookings.
"""

from collections import OrderedDict
from datetime import date, datetime, timedelta

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404

from .forms import BookingForm, ReviewForm
from .models import Booking, Review


def home(request):
    """
    Отображает главную страницу сайта.
    Показывает последние одобренные отзывы.
    """
    approved_reviews = Review.objects.filter(approved=True).order_by('-created_at')
    return render(request, 'bookings/home.html', {
        'approved_reviews': approved_reviews,
    })


def check_capacity(new_booking):
    """
    Проверяет, хватает ли места на выбранную дату и время
    с учётом 2-часового окна бронирования.

    Аргументы:
        new_booking: объект бронирования (не сохранённый в базе).

    Возвращает:
        Общее количество забронированных мест за выбранное время.
    """
    booking_date = new_booking.date
    new_start = datetime.combine(booking_date, new_booking.time)
    new_end = new_start + timedelta(hours=2)

    existing_bookings = Booking.objects.filter(date=booking_date)
    total_reserved = 0

    for booking in existing_bookings:
        existing_start = datetime.combine(booking.date, booking.time)
        existing_end = existing_start + timedelta(hours=2)
        if new_start < existing_end and existing_start < new_end:
            total_reserved += booking.guests

    return total_reserved


def book_table(request):
    """
    Обрабатывает форму бронирования. Проверяет доступность мест,
    сохраняет бронирование, отправляет подтверждающее письмо и
    перенаправляет на страницу успеха.

    Возвращает:
        Отображение формы бронирования или перенаправление к успеху.
    """
    initial_data = {}
    if 'time' in request.GET:
        initial_data['time'] = request.GET.get('time')

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            new_booking = form.save(commit=False)
            total_reserved = check_capacity(new_booking)
            allowed_capacity = 40  # 80% от 50 мест

            if total_reserved + new_booking.guests > allowed_capacity:
                form.add_error(
                    None,
                    "Невозможно забронировать: Данный временной интервал почти заполнен."
                )
                return render(request, 'bookings/book_table.html', {'form': form})

            new_booking.save()
            messages.success(request,
                             f'Ваше бронирование на {new_booking.date} в {new_booking.time} подтверждено!')
            send_mail(
                subject="Подтверждение бронирования",
                message=(
                    f"Уважаемый {new_booking.name},\n\n"
                    f"Ваше бронирование на {new_booking.date} в {new_booking.time} подтверждено."
                ),
                from_email="noreply@site.com",
                recipient_list=[new_booking.email],
            )
            return redirect('booking_success', booking_id=new_booking.id)
    else:
        form = BookingForm(initial=initial_data)

    return render(request, 'bookings/book_table.html', {'form': form})


def booking_success(request, booking_id):
    """
    Отображает страницу успешного бронирования с деталями.
    """
    booking = Booking.objects.get(id=booking_id)
    return render(request, 'bookings/booking_success.html', {'booking': booking})


def available_timeslots(request):
    """
    Показывает доступные временные интервалы.
    Для демонстрации интервалы жестко заданные.
    """
    timeslots = [
        {'time': '18:00', 'available': True},
        {'time': '18:30', 'available': False},
        {'time': '19:00', 'available': True},
        {'time': '19:30', 'available': True},
        {'time': '20:00', 'available': False},
    ]
    return render(request, 'bookings/timeslots.html', {'timeslots': timeslots})


@staff_member_required
def booking_list(request):
    """
    Отображает список всех бронирований.
    Доступно только для сотрудников.
    """
    bookings = Booking.objects.all().order_by('-id')
    return render(request, 'bookings/booking_list.html', {'bookings': bookings})


@staff_member_required
def weekly_calendar(request):
    """
    Отображает недельный календарь бронирований. 
    Только для сотрудников.
    """
    week_start_str = request.GET.get("week_start")
    if week_start_str:
        try:
            week_start = datetime.strptime(week_start_str, "%Y-%m-%d").date()
        except ValueError:
            week_start = date.today() - timedelta(days=date.today().weekday())
    else:
        week_start = date.today() - timedelta(days=date.today().weekday())

    bookings_by_day = OrderedDict()
    for i in range(7):
        current_day = week_start + timedelta(days=i)
        daily_bookings = Booking.objects.filter(date=current_day).order_by('time')
        bookings_by_day[current_day] = daily_bookings

    previous_week = week_start - timedelta(days=7)
    next_week = week_start + timedelta(days=7)

    return render(request, 'bookings/weekly_calendar.html', {
        'week_start': week_start,
        'bookings_by_day': bookings_by_day,
        'previous_week': previous_week.strftime("%Y-%m-%d"),
        'next_week': next_week.strftime("%Y-%m-%d"),
    })


def cancel_booking(request, booking_id):
    """
    Отмена бронирования после проверки email клиента.
    """
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == 'POST':
        email_input = request.POST.get('email')
        if email_input and email_input.lower() == booking.email.lower():
            booking.delete()
            messages.success(request, "Ваше бронирование отменено.")
            return redirect('home')
        else:
            messages.error(request, "Введённый email не найден.")

    return render(request, 'bookings/cancel_booking.html', {'booking': booking})


def confirm_cancel(request, booking_id):
    """
    Отображает страницу подтверждения отмены бронирования.
    Если пользователь подтверждает, бронирование удаляется, и выводится сообщение об успехе.

    Аргументы:
        request: объект HTTP-запроса.
        booking_id: ID бронирования для отмены.

    Возвращает:
        GET: страницу подтверждения отмены.
        POST: удаляет бронирование и перенаправляет на главную страницу.
    """
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == 'POST':
        # Удалить бронирование и вывести сообщение об успехе
        booking.delete()
        messages.success(request, "Спасибо, надеемся скоро снова увидеть вас!")
        return redirect('home')  # Перенаправляем на главную страницу

    # Отображение страницы подтверждения отмены (GET-запрос)
    return render(request, 'bookings/cancel_confirm.html', {'booking': booking})


def update_booking_lookup(request):
    """
    Отображает форму для поиска бронирования по электронной почте.
    Если бронирования найдены, выводится их список с возможностью изменения.

    Аргументы:
        request: объект HTTP-запроса.

    Возвращает:
        Отображение формы поиска или список найденных бронирований.
    """
    bookings_found = None
    if request.method == 'POST':
        email = request.POST.get('email')  # Считываем email из запроса
        if email:
            bookings_found = Booking.objects.filter(email__iexact=email)
            if not bookings_found:
                messages.error(request,
                               "Для этого адреса электронной почты бронирования не найдены.")
        else:
            messages.error(request, "Пожалуйста, введите адрес электронной почты.")

    return render(request, 'bookings/update_booking_lookup.html', {
        'bookings_found': bookings_found
    })


def submit_review(request):
    """
    Обрабатывает форму для отправки отзыва.
    Отзывы остаются в ожидании подтверждения администратором.

    Аргументы:
        request: объект HTTP-запроса.

    Возвращает:
        GET: Пустую форму для отправки отзыва.
        POST: Сохраняет отправленный отзыв, выводит сообщение об успешной отправке.
    """
    if request.method == 'POST':
        form = ReviewForm(request.POST)  # Обрабатываем данные из формы на отправку отзыва
        if form.is_valid():
            form.save()  # Сохраняем новый отзыв
            messages.success(request,
                             "Спасибо за ваш отзыв! Он появится на сайте после подтверждения.")
            return redirect('home')  # Перенаправляем на главную страницу
    else:
        form = ReviewForm()

    return render(request, 'bookings/submit_review.html', {'form': form})


def review_ticker(request):
    """
    Получает список одобренных отзывов для дисплея в виде тикера.

    Аргументы:
        request: объект HTTP-запроса.

    Возвращает:
        Шаблон, содержащий список одобренных отзывов.
    """
    reviews = Review.objects.filter(approved=True).order_by(
        '-created_at')  # Получаем все одобренные отзывы
    return render(request, 'bookings/review_ticker.html', {'reviews': reviews})


def update_booking(request, booking_id):
    """
    Позволяет клиенту изменить или перенести бронирование после подтверждения email.
    Форма предварительно заполняется данными текущего бронирования.

    Аргументы:
        request: объект HTTP-запроса.
        booking_id: ID бронирования, которое нужно изменить.

    Возвращает:
        GET: Форма с данными текущего бронирования.
        POST: Обновляет данные бронирования после проверки и перенаправляет.
    """
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == 'POST':
        # Проверяем подтверждение email для изменения
        confirm_email = request.POST.get('confirm_email')
        if not confirm_email or confirm_email.lower() != booking.email.lower():
            messages.error(request,
                           "Указанная электронная почта не соответствует записанным данным.")
        else:
            form = BookingForm(request.POST,
                               instance=booking)  # Сохраняем изменения в существующую запись
            if form.is_valid():
                updated_booking = form.save()
                messages.success(request, "Ваше бронирование успешно обновлено!")
                return redirect('booking_success', booking_id=updated_booking.id)
            else:
                messages.error(request, "Пожалуйста, исправьте ошибки ниже.")
    else:
        form = BookingForm(instance=booking)  # Предзаполняем форму существующими данными

    return render(request, 'bookings/update_booking.html', {
        'form': form,
        'booking': booking
    })


def cancel_booking(request, booking_id):
    """
    Позволяет клиенту отменить своё бронирование, если указан правильный email.
    Загружает бронирование по ID.
    На POST-запрос сравнивает email пользователя с email бронирования.
    Если адреса email совпадают, бронирование удаляется и выводится сообщение об успехе,
    иначе — сообщение об ошибке.
    На GET-запрос отображает страницу подтверждения отмены.

    Аргументы:
        request: объект HTTP-запроса.
        booking_id: ID бронирования для отмены.

    Возвращает:
        GET: Отображение страницы подтверждения отмены.
        POST: Удаляет бронирование, если email пользователя совпадает с тем, что указан в записи.
    """
    # Получаем бронирование или выдаём ошибку 404, если его нет
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == 'POST':
        # Считываем email пользователя из формы отмены бронирования
        email_input = request.POST.get('email')

        # Сравниваем email пользователя с email бронирования (игнорируя регистр)
        if email_input and email_input.lower() == booking.email.lower():
            booking.delete()  # Удаляем бронирование
            messages.success(request, "Ваше бронирование было отменено.")
            return redirect('home')  # Перенаправляем на главную страницу
        else:
            messages.error(request,
                           "Введённый адрес электронной почты не совпадает с нашими записями.")

    # Отображаем страницу подтверждения отмены
    return render(request, 'bookings/cancel_booking.html', {'booking': booking})


def cancel_lookup(request):
    """
    Отображает форму для поиска текущих бронирований по email для их отмены.

    Аргументы:
        request: объект HTTP-запроса.

    Возвращает:
        GET: Пустая форма для ввода email.
        POST: Список бронирований для указанной электронной почты.
    """
    bookings_found = None
    if request.method == 'POST':
        email = request.POST.get('email')  # Получаем email из запроса
        if email:
            bookings_found = Booking.objects.filter(
                email__iexact=email)  # Ищем бронирования по email
            if not bookings_found:
                messages.error(request,
                               "Для этого адреса электронной почты бронирования не найдены.")
        else:
            messages.error(request, "Пожалуйста, укажите адрес электронной почты.")

    return render(request, 'bookings/cancel_lookup.html', {
        'bookings_found': bookings_found
    })
