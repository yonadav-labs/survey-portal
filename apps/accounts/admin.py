from django import forms
from django.conf import settings
from django.contrib import admin
from django.contrib.admin.sites import NotRegistered
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import (ReadOnlyPasswordHashField,
                                       AdminPasswordChangeForm,
                                       UserCreationForm)
from django.contrib.auth.models import Group
from .models import EmailUser


class SettingsUserForAdmin:
    def __init__(self, *args, **kwargs):
        if not getattr(self.Meta, 'model'):
            self.Meta.model = get_user_model()
        super().__init__(*args, **kwargs)


class UserChangeForm(SettingsUserForAdmin, forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField(
        label="Password",
        help_text=("Raw passwords are not stored, so there is no way to see "
                   "this user's password, but you can change the password "
                   "using <a href=\"password/\">this form</a>."))

    class Meta:
        # the model attribute will be set by
        # SettingsUserForAdmin.__init__() - see that method
        fields = ('email', 'password')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class MyUserCreationForm(SettingsUserForAdmin,
                         UserCreationForm):
    class Meta:
        # the model attribute will be set by
        # SettingsUserForAdmin.__init__() - see that method
        fields = ("email",)

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            get_user_model().objects.get(email=email)
        except get_user_model().DoesNotExist:
            return email
        raise forms.ValidationError(self.error_messages['duplicate_email'])


class EmailUserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = MyUserCreationForm
    change_password_form = AdminPasswordChangeForm
    actions_on_bottom = True
    ordering = ('first_name',)
    list_filter = ('is_active',)
    autocomplete_fields = ('representative',)
    list_display = ('email', 'first_name', 'last_name', 'phone', 'is_superuser')
    search_fields = ('email', 'last_name', 'first_name')
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    fieldsets = (
        ('User Info', {
            'fields': (
                'email', 'password',
                ('last_login', 'date_joined'),
                ('first_name', 'middle_name', 'last_name'),
                ('phone',),
                'is_active',
            ),
        }),
        ('Roles', {
            'fields': (
                'is_superuser',
                'representative',
                'groups',
                'user_permissions'
            ),
        })
    )


admin.site.register(EmailUser, EmailUserAdmin)
