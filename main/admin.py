from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from main.models import Hospital, UserProfile, Visit


class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = UserProfile


class MyUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = UserProfile


ADDITIONAL_FIELDS_USER = (
    ('Personal info', {'fields': ('gender', 'role', 'phone_number', 'birthday',
                                  'city', 'street', 'zip_code', 'hospital')}),
)


class MyUserAdmin(UserAdmin):
    form = MyUserChangeForm
    add_form = MyUserCreationForm

    fieldsets = UserAdmin.fieldsets + ADDITIONAL_FIELDS_USER
    add_fieldsets = UserAdmin.add_fieldsets + ADDITIONAL_FIELDS_USER


admin.site.register(UserProfile, MyUserAdmin)
admin.site.register(Hospital)
admin.site.register(Visit)
