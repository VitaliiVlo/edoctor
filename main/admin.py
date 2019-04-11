from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm

from main.models import Hospital, UserProfile, Visit


class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = UserProfile


class MyUserAdmin(UserAdmin):
    form = MyUserChangeForm

    fieldsets = UserAdmin.fieldsets + (
        ('Personal info', {'fields': ('gender', 'role', 'phone_number', 'birthday', 'city', 'street', 'zip_code',
                                      'hospital')}),
    )


admin.site.register(UserProfile, MyUserAdmin)
admin.site.register(Hospital)
admin.site.register(Visit)
