# from django.shortcuts import render
# from django.urls import reverse_lazy
from django.db.models import Q

from cms.views import BaseList, BaseDetail, BaseCreate, BaseUpdate, BaseDelete


from .models import AccountType, Project, Password
from .forms import AccountTypeForm, ProjectForm, PasswordForm


class AccountTypeList(BaseList):
    model = AccountType
    paginate_by = 100

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q')
        if q and q != '':
            qs = qs.filter(name__icontains=q)
        return qs


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


class ProjectList(BaseList):
    model = Project
    paginate_by = 100

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q')
        if q and q != '':
            qs = qs.filter(name__icontains=q)
        return qs


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


class PasswordList(BaseList):
    model = Password
    paginate_by = 100

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q')
        if q and q != '':
            qs = qs.filter(
                Q(project__name__icontains=q) |
                Q(account_type__name__icontains=q) | Q(username__icontains=q)
            )
        return qs


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
