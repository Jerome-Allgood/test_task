from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from .models import Restaurant, CustomUser, Reserved, PreOrder


# Register your models here.
@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'phone', 'address', 'email']


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    """Define admin model for custom User model with no email field."""
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'phone')}),
        (_('Permissions'),
         {'fields': ('is_active', 'is_staff', 'is_superuser',
                     'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'phone', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


@admin.register(Reserved)
class ReservedAdmin(admin.ModelAdmin):
    list_display = ['id', 'restaurant', 'user', 'preorder']


@admin.register(PreOrder)
class PreOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'restaurant', 'user', 'status']
