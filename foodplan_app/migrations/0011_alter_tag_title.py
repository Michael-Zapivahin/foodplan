# Generated by Django 4.2.4 on 2023-09-30 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodplan_app', '0010_auto_20230930_1536'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='title',
            field=models.CharField(max_length=50, unique=True, verbose_name='Title'),
        ),
    ]
