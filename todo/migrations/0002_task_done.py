# Generated by Django 3.2.23 on 2024-01-23 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='done',
            field=models.BooleanField(default=False, verbose_name='완료상태'),
        ),
    ]