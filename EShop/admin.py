from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import SiteUser, BuyerUser, DeveloperUser, Product, Tag, Genre, ProductImage


# Register your models here.


class SiteUserAdminInline(admin.StackedInline):
    extra = 0
    model = BuyerUser
    can_delete = False


class DeveloperAdminInline(admin.StackedInline):
    extra = 0
    model = DeveloperUser
    can_delete = False


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = [SiteUserAdminInline, DeveloperAdminInline]


class ImageProductAdminInline(admin.StackedInline):
    extra = 0
    model = ProductImage




class ProductAdmin(admin.ModelAdmin):
    inlines = [ImageProductAdminInline,]


class BuyerUserAdmin(admin.ModelAdmin):
    list_display = ["user"]


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Tag)
admin.site.register(Genre)

admin.site.register(DeveloperUser)
admin.site.register(BuyerUser, BuyerUserAdmin)
