# from django.shortcuts import render
from django.urls import reverse_lazy
from django.db.models import Q
from django.http import HttpResponseRedirect

from cms.views import BaseList, BaseDetail, BaseCreate, BaseUpdate, BaseDelete


from .models import AccountType, Project, Password
from .forms import AccountTypeForm, ProjectForm, PasswordForm


class ActiveMixin:
    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.active = False
        obj.save()
        return HttpResponseRedirect(self.success_url)


class AccountTypeList(BaseList):
    model = AccountType
    paginate_by = 100

    def get_queryset(self):
        qs = super().get_queryset().active()
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


class AccountTypeDelete(ActiveMixin, BaseDelete):
    model = AccountType
    success_url = reverse_lazy('accounttype-list')


class ProjectList(BaseList):
    model = Project
    paginate_by = 100

    def get_queryset(self):
        qs = super().get_queryset().active()
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


class ProjectDelete(ActiveMixin, BaseDelete):
    model = Project
    success_url = reverse_lazy('project-list')


class PasswordList(BaseList):
    model = Password
    paginate_by = 100

    def get_queryset(self):
        qs = super().get_queryset().active()
        active_projects_pk = set()
        active_account_types_pk = set()
        for project in Project.objects.active():
            active_projects_pk.add(project.pk)
        for account_type in AccountType.objects.active():
            active_account_types_pk.add(account_type.pk)
        qs = qs.filter(
            Q(project_id__in=active_projects_pk) |
            Q(account_type_id__in=active_account_types_pk))
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


class PasswordDelete(ActiveMixin, BaseDelete):
    model = Password
    success_url = reverse_lazy('password-list')
