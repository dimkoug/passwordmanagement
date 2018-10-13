from django.contrib import admin
from django.conf import settings
from .models import AccountType, Project, Password
from .aescbc import decrypt
# Register your models here.


def delete_model(modeladmin, request, queryset):
    for obj in queryset:
        obj.active = False
        obj.save()


class BaseAdmin(admin.ModelAdmin):
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


class AccountTypeAdmin(BaseAdmin):
    model = AccountType
    list_display = ('name', 'active')
    list_filter = ('name', 'active')
    actions = [delete_model]


class ProjectAdmin(BaseAdmin):
    model = Project
    list_display = ('name', 'active')
    list_filter = ('name', 'active')
    actions = [delete_model]


class PasswordAdmin(BaseAdmin):
    list_display = (
        'username', 'account_type', 'project', 'view_password', 'active'
    )
    search_fields = ['username', 'project__name', 'account_type__name']
    list_filter = ('account_type', 'project', 'active')
    actions = [delete_model]

    def view_password(self, obj):
        decrypted = decrypt(bytes(settings.SECRET_KEY, 'utf-8'), obj.password)
        return decrypted.decode("utf-8")


admin.site.register(AccountType, AccountTypeAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Password, PasswordAdmin)
