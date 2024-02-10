from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone

from accounts.models import Profile


class Category(models.Model):
    name = models.CharField(max_length=31, verbose_name='Категория', blank=False)

    def __str__(self):
        return self.name


class Project(models.Model):
    STATUS_CHOICES = [
        ('to_moderation', 'На модерацию'),
        ('published', 'Опубликовано'),
        ('rejected', 'Отклонено'),
        ('to_delete', 'На удаление')
    ]
    picture = models.ImageField(upload_to='project_pictures', null=True, blank=True, verbose_name='Картинка')
    title = models.CharField(max_length=50, verbose_name='Заголовок', blank=False)
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='projects', verbose_name='Автор объявления')
    category = models.ManyToManyField('webapp.Category', related_name='projects', verbose_name='Категории')
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], verbose_name='Цена', blank=False)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='to_moderation', verbose_name='Статус')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now_add=True, verbose_name='Дата изменения')
    published_at = models.DateTimeField(null=True, blank=True, verbose_name='Дата-время публикации')

    def save(self, *args, **kwargs):
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'({self.id}) {self.author} - {self.title}'


class Review(models.Model):
    text = models.TextField(verbose_name='Текст отзыва', blank=False)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='reviews', verbose_name='Автор отзыва')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='reviews', verbose_name='Объявление', blank=False)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f'{self.text} ({self.id})'
