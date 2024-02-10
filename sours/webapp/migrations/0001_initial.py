# Generated by Django 5.0.2 on 2024-02-10 06:19

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=31, verbose_name='Категория')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(blank=True, null=True, upload_to='project_pictures', verbose_name='Картинка')),
                ('title', models.CharField(max_length=50, verbose_name='Заголовок')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Цена')),
                ('status', models.CharField(choices=[('to_moderation', 'На модерацию'), ('published', 'Опубликовано'), ('rejected', 'Отклонено'), ('to_delete', 'На удаление')], default='to_moderation', max_length=50, verbose_name='Статус')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Дата изменения')),
                ('published_at', models.DateTimeField(blank=True, null=True, verbose_name='Дата-время публикации')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='accounts.user', verbose_name='Автор объявления')),
                ('category', models.ManyToManyField(related_name='projects', to='webapp.category', verbose_name='Категории')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Текст отзыва')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='accounts.user', verbose_name='Автор отзыва')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='webapp.project', verbose_name='Объявление')),
            ],
        ),
    ]