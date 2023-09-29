from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Dish,
    Component,
    Menu,
    Allergy,
    Client,
    Subscription,
    SubscriptionAllergy,
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
    image_tag.short_description = 'Photo'
    list_display = ['title', 'image_tag']
    ordering = ['title']


@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    list_display = ['title', 'dish']
    ordering = ['dish']


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    pass


@admin.register(Allergy)
class AllergyAdmin(admin.ModelAdmin):
    pass


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    pass


class AllergyInline(admin.TabularInline):
    extra = 0
    model = SubscriptionAllergy


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    inlines = [AllergyInline,]


@admin.register(SubscriptionAllergy)
class SubscriptionAllergyAdmin(admin.ModelAdmin):
    pass

