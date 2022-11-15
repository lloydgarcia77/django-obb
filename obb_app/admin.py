from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.sessions.models import Session
from .forms import UserAdminCreationForms, UserAdminChangeForm
from . import models

admin.site.site_header = 'Online Bus Booking Super Administrator'
admin.site.index_title = 'Super Administrator Page'
admin.site.site_title = 'Super Administrator Panel'

User = get_user_model()

# NOTE: Only is_super user allows to go this admin page
#! https://stackoverflow.com/questions/19045000/django-admin-site-register-only-for-superuser
def has_superuser_permission(request):
    return request.user.is_active and request.user.is_staff and request.user.is_superuser

admin.site.has_permission = has_superuser_permission

admin.site.unregister(Group)



class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()
    list_display = ['session_key', '_session_data', 'expire_date']


admin.site.register(Session, SessionAdmin)


class UserAdmin(BaseUserAdmin):
    # the forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForms

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ['email', 'is_staff',
                    'is_active', 'is_superuser', 'is_valid']
    list_filter = ['is_staff']

    fieldsets = (
        ("Account", {
            'fields':
                (
                    'email',
                    'password',
                )
        }),

     

        ('Permission', {
            'fields': (
                'is_staff',
                'is_active',
                'is_superuser',
                'is_valid'
            )
        }),
    )

    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.

    add_fieldsets = (
  
        ('Permission', {
            'fields': (
                'is_staff',
                'is_active',
                'is_superuser',
                'is_valid'
            )
        }),
        (
            "Account", {
                'classes': ('wide', ),
                'fields': ('email', 'password', 'password_2')
            }
        ),
    )

    search_fields = ['email']
    ordering = ['email']
    filter_horizontal = ()


admin.site.register(User, UserAdmin)

