from django import forms

from core.forms import BootstrapForm

from .models import AccountType, Project, Password


class AccountTypeForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = AccountType
        fields = ('name','active')


class ProjectForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Project
        fields = ('name','active')


class PasswordForm(BootstrapForm, forms.ModelForm):
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
