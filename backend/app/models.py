# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    """
    Расширенная модель пользователя.
    Добавляем дополнительные поля по мере необходимости.
    """
    # Пример дополнительных полей
    display_name = models.CharField(max_length=150, blank=True, null=True, verbose_name=_("Display name"))
    clan = models.ForeignKey('Clans', on_delete=models.SET_NULL, related_name='members', blank=True, null=True)

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return self.get_full_name() or self.username


class Clans(models.Model):
    """
    Модель кланов/гильдий.
    Один клан может иметь много участников (Users).
    """
    name = models.CharField(max_length=100, unique=True)
    motto = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Можно добавить атрибуты/метаданные
    class Meta:
        verbose_name = _("clan")
        verbose_name_plural = _("clans")

    def __str__(self):
        return self.name


class Characteristics(models.Model):
    """
    Характеристики персонажа или других объектов.
    Связаны с User и/или с Tasks/Targets по необходимости.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='characteristics', null=True, blank=True)
    strength = models.PositiveIntegerField(default=0)
    agility = models.PositiveIntegerField(default=0)
    intelligence = models.PositiveIntegerField(default=0)
    stamina = models.PositiveIntegerField(default=0)

    # Пример связи с задачей/целью (опционально)
    # task = models.ForeignKey('Tasks', on_delete=models.SET_NULL, null=True, blank=True, related_name='characteristics')

    class Meta:
        verbose_name = _("characteristics")
        verbose_name_plural = _("characteristics")

    def __str__(self):
        parts = [str(self.strength), str(self.agility), str(self.intelligence)]
        return "Characteristics(" + ", ".join(parts) + ")"


class Tasks(models.Model):
    """
    Задачи/миссии персонажа.
    """
    STATUS_CHOICES = [
        ('PENDING', _("Pending")),
        ('IN_PROGRESS', _("In progress")),
        ('COMPLETED', _("Completed")),
        ('FAILED', _("Failed")),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='tasks', null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Дополнительные поля по мере необходимости
    # related_characteristics = models.ForeignKey(Characteristics, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')

    class Meta:
        verbose_name = _("task")
        verbose_name_plural = _("tasks")

    def __str__(self):
        return self.title


class Targets(models.Model):
    """
    Цели/достижения.
    Может быть привязана к пользователю или к задаче.
    """
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='targets')
    due_date = models.DateField(null=True, blank=True)
    is_achieved = models.BooleanField(default=False)

    # Привязка к задаче или характеристикам (по мере необходимости)
    task = models.ForeignKey(Tasks, on_delete=models.SET_NULL, null=True, blank=True, related_name='targets')
    characteristics = models.ForeignKey(Characteristics, on_delete=models.SET_NULL, null=True, blank=True, related_name='targets')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("target")
        verbose_name_plural = _("targets")

    def __str__(self):
        return self.name