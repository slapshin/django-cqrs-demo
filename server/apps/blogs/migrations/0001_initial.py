# Generated by Django 4.0.4 on 2022-05-10 13:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, help_text='HT__TITTE', max_length=50, unique=True, verbose_name='VN__TITLE')),
                ('content', models.TextField(blank=True, help_text='HT__CONTENT', verbose_name='VN__CONTENT')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='HT__CREATED_AT', verbose_name='VN__CREATED_AT')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='HT__UPDATED_AT', verbose_name='VN__UPDATED_AT')),
                ('author', models.ForeignKey(help_text='HT__AUTHOR', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='VN__AUTHOR')),
            ],
            options={
                'verbose_name': 'VN__POST',
                'verbose_name_plural': 'VN__POSTS',
                'unique_together': {('author', 'title')},
            },
        ),
    ]
