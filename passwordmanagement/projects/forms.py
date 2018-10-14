from django import forms

from cms.forms import DynamicForm

from .models import AccountType, Project, Password


class AccountTypeForm(DynamicForm, forms.ModelForm):
    class Meta:
        model = AccountType
        fields = ('name',)


class ProjectForm(DynamicForm, forms.ModelForm):
    class Meta:
        model = Project
        fields = ('name',)


class PasswordForm(DynamicForm, forms.ModelForm):
    class Meta:
        model = Password
        fields = (
            'account_type', 'project', 'username', 'password', 'url',
            'comments'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.initial['password'] = self.instance.get_password()
