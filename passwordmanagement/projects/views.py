from django.shortcuts import render
from django.urls import reverse_lazy
from django.db.models import Q

from cms.views import BaseList, BaseDetail, BaseCreate, BaseUpdate, BaseDelete


from .forms import AccountTypeForm, ProjectForm, PasswordForm
from .models import AccountType, Project, Password
from .mixins import ProtectedViewMixin, SaveProfileMixin, ActiveMixin


class AccountTypeList(ProtectedViewMixin, BaseList):
    model = AccountType
    paginate_by = 100

    def get_queryset(self):
        qs = super().get_queryset().active().filter(
            profile=self.request.user.profile_user)
        q = self.request.GET.get('q')
        if q and q != '':
            qs = qs.filter(name__icontains=q)
        return qs


class AccountTypeDetail(ProtectedViewMixin, BaseDetail):
    model = AccountType


class AccountTypeCreate(ProtectedViewMixin, SaveProfileMixin, BaseCreate):
    model = AccountType
    form_class = AccountTypeForm


class AccountTypeUpdate(ProtectedViewMixin, BaseUpdate):
    model = AccountType
    form_class = AccountTypeForm


class AccountTypeDelete(ProtectedViewMixin, ActiveMixin, BaseDelete):
    model = AccountType
    success_url = reverse_lazy('accounttype-list')


class ProjectList(ProtectedViewMixin, BaseList):
    model = Project
    paginate_by = 100

    def get_queryset(self):
        qs = super().get_queryset().active().filter(
            profile=self.request.user.profile_user)
        q = self.request.GET.get('q')
        if q and q != '':
            qs = qs.filter(name__icontains=q)
        return qs


class ProjectDetail(ProtectedViewMixin, BaseDetail):
    model = Project


class ProjectCreate(ProtectedViewMixin, SaveProfileMixin, BaseCreate):
    model = Project
    form_class = ProjectForm


class ProjectUpdate(ProtectedViewMixin, BaseUpdate):
    model = Project
    form_class = ProjectForm


class ProjectDelete(ProtectedViewMixin, ActiveMixin, BaseDelete):
    model = Project
    success_url = reverse_lazy('project-list')


class PasswordList(ProtectedViewMixin, BaseList):
    model = Password
    paginate_by = 100

    def get_queryset(self):
        qs = super().get_queryset().active().filter(
            profile=self.request.user.profile_user)
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


class PasswordDetail(ProtectedViewMixin, BaseDetail):
    model = Password


class PasswordCreate(ProtectedViewMixin, SaveProfileMixin, BaseCreate):
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


class PasswordUpdate(ProtectedViewMixin, BaseUpdate):
    model = Password
    form_class = PasswordForm


class PasswordDelete(ProtectedViewMixin, ActiveMixin, BaseDelete):
    model = Password
    success_url = reverse_lazy('password-list')
