from django.shortcuts import render
from django.urls import reverse_lazy

from cms.views import BaseList, BaseDetail, BaseCreate, BaseUpdate, BaseDelete


from .models import AccountType, Project, Password
from .forms import AccountTypeForm, ProjectForm, PasswordForm

# Create your views here.


class AccountTypeList(BaseList):

    model = AccountType
    paginate_by = 100  # if pagination is desired


class AccountTypeDetail(BaseDetail):
    model = AccountType


class AccountTypeCreate(BaseCreate):
    model = AccountType
    form_class = AccountTypeForm


class AccountTypeUpdate(BaseUpdate):
    model = AccountType
    form_class = AccountTypeForm


class AccountTypeDelete(BaseDelete):
    model = AccountType
    success_url = reverse_lazy('accounttype-list')


class ProjectList(BaseList):

    model = Project
    paginate_by = 100  # if pagination is desired


class ProjectDetail(BaseDetail):
    model = Project


class ProjectCreate(BaseCreate):
    model = Project
    form_class = ProjectForm


class ProjectUpdate(BaseUpdate):
    model = Project
    form_class = ProjectForm


class ProjectDelete(BaseDelete):
    model = Project
    success_url = reverse_lazy('project-list')


class PasswordList(BaseList):

    model = Password
    paginate_by = 100  # if pagination is desired


class PasswordDetail(BaseDetail):
    model = Password


class PasswordCreate(BaseCreate):
    model = Password
    form_class = PasswordForm

    def get_initial(self):
        initial = super().get_initial()
        if 'accounttype' in self.request.GET:
            initial.update({
                'account_type': self.request.GET.get('accounttype')
            })
        if 'project' in self.request.GET:
            initial.update({
                'project': self.request.GET.get('project')
            })
        return initial


class PasswordUpdate(BaseUpdate):
    model = Password
    form_class = PasswordForm


class PasswordDelete(BaseDelete):
    model = Password
    success_url = reverse_lazy('password-list')
