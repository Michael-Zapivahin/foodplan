# Generated by Django 3.2.15 on 2023-09-28 06:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('photo', models.ImageField(blank=True, max_length=200, null=True, upload_to='', verbose_name='Photo')),
                ('calories', models.IntegerField(blank=True, null=True, verbose_name='Calories')),
            ],
        ),
        migrations.CreateModel(
            name='Component',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('weight', models.IntegerField(blank=True, null=True, verbose_name='weight')),
                ('dish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dishes', to='foodplan_app.dish', verbose_name='dish')),
            ],
        ),
    ]