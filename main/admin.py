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
    ('Personal info 2', {'fields': ('gender', 'role', 'phone_number', 'birthday',
                                    'city', 'street', 'zip_code', 'hospital')}),
)

CHANGE_FIELD_SET = (
    (None, {'fields': ('email', 'username', 'password')}),
    ('Personal info', {'fields': ('first_name', 'last_name')}),
    ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
)

ADD_FIELD_SET = (
    (None, {
        'classes': ('wide',),
        'fields': ('email', 'username', 'password1', 'password2'),
    }),
)


class MyUserAdmin(UserAdmin):
    form = MyUserChangeForm
    add_form = MyUserCreationForm

    fieldsets = CHANGE_FIELD_SET + ADDITIONAL_FIELDS_USER
    add_fieldsets = ADD_FIELD_SET + ADDITIONAL_FIELDS_USER
    list_display = ('email', 'first_name', 'last_name', 'is_staff')


admin.site.register(UserProfile, MyUserAdmin)
admin.site.register(Hospital)
admin.site.register(Visit)
