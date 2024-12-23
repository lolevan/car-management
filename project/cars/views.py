from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Car

from .forms import CommentForm, CarForm



def car_list(request):
    """ Список автомобилей (главная страница) """
    cars = Car.objects.all().order_by('-created_at')
    return render(request, 'cars/car_list.html', {'cars': cars})


def car_detail(request, car_id):
    """ Детальная страница автомобиля + список комментариев """
    car = get_object_or_404(Car, id=car_id)
    comments = car.comments.all().order_by('-created_at')

    # Обработка добавления комментария
    if request.method == 'POST':
        if not request.user.is_authenticated:
            # Только зарегистрированные могут комментировать
            raise PermissionDenied("Вы должны быть авторизованы, чтобы комментировать.")
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.car = car
            comment.save()
            return redirect('car_detail', car_id=car.id)
    else:
        form = CommentForm()

    return render(request, 'cars/car_detail.html', {
        'car': car,
        'comments': comments,
        'form': form
    })


@login_required
def car_create(request):
    """ Создание нового автомобиля (доступно только аутентифицированным пользователям) """
    if request.method == 'POST':
        form = CarForm(request.POST)
        if form.is_valid():
            car = form.save(commit=False)
            car.owner = request.user
            car.save()
            return redirect('car_detail', car_id=car.id)
    else:
        form = CarForm()
    return render(request, 'cars/car_form.html', {'form': form, 'title': 'Добавить автомобиль'})


@login_required
def car_update(request, car_id):
    """ Редактирование автомобиля (только владелец) """
    car = get_object_or_404(Car, id=car_id)
    if car.owner != request.user:
        raise PermissionDenied("У вас нет прав на редактирование этого автомобиля.")

    if request.method == 'POST':
        form = CarForm(request.POST, instance=car)
        if form.is_valid():
            form.save()
            return redirect('car_detail', car_id=car.id)
    else:
        form = CarForm(instance=car)
    return render(request, 'cars/car_form.html', {'form': form, 'title': 'Редактировать автомобиль'})


@login_required
def car_delete(request, car_id):
    """ Удаление автомобиля (только владелец) """
    car = get_object_or_404(Car, id=car_id)
    if car.owner != request.user:
        raise PermissionDenied("У вас нет прав на удаление этого автомобиля.")

    if request.method == 'POST':
        car.delete()
        return redirect('car_list')

    # Для подтверждения удаления можно отрендерить отдельный шаблон
    return render(request, 'cars/car_delete_confirm.html', {'car': car})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('car_list')
    else:
        form = UserCreationForm()
    return render(request, 'cars/register.html', {'form': form})
