from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Dish,
    Component
)

# Register your models here.

@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    def image_tag(self, dish):
        return format_html(
            '<img style="max-height:{height}" src="{url}"/>',
            url=dish.photo.url,
            height='100px',
        )


@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    pass
