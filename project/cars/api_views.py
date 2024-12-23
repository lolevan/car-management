from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Car, Comment
from .serializers import CarSerializer, CommentSerializer


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Разрешение, позволяющее редактировать объект только его владельцу.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user


class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        # При создании нового автомобиля установить owner = текущий пользователь
        serializer.save(owner=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # При создании комментария установить author = текущий пользователь
        serializer.save(author=self.request.user)

    def get_queryset(self):
        """
        Если мы хотим, чтобы комментарии выводились только в контексте
        конкретного автомобиля, можно фильтровать по параметру car_id из URL.
        Но в задании есть отдельная точка для получения комментариев
        к конкретному автомобилю – покажем это через дополнительный метод.
        """
        return super().get_queryset()

