from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.template.loader import render_to_string
from django.db.models import Prefetch, Q
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView


from core.functions import is_ajax
from core.mixins import PaginationMixin, ModelMixin, SuccessUrlMixin,FormMixin,QueryListMixin, AjaxDeleteMixin


from .forms import AccountTypeForm, ProjectForm, PasswordForm
from .models import AccountType, Project, Password


class BaseListView(PaginationMixin,QueryListMixin,ModelMixin, LoginRequiredMixin, ListView):
    def dispatch(self, *args, **kwargs):
        self.ajax_list_partial = '{}/partials/{}_list_partial.html'.format(self.model._meta.app_label,self.model.__name__.lower())
        return super().dispatch(*args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        if is_ajax(request):
            html_form = render_to_string(
                self.ajax_list_partial, context, request)
            return JsonResponse(html_form, safe=False)
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(profile_id=self.request.user.profile.id)
        return queryset


class AccountTypeList(BaseListView):
    model = AccountType
    paginate_by = 100
    queryset = AccountType.objects.select_related('profile')

    def get_queryset(self):
        qs = super().get_queryset().active().filter(
            profile=self.request.user.profile)
        q = self.request.GET.get('q')
        if q and q != '':
            qs = qs.filter(name__icontains=q)
        return qs


class AccountTypeDetail(LoginRequiredMixin, DetailView):
    model = AccountType
    queryset = AccountType.objects.select_related('profile')

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(profile_id=self.request.user.profile.id)
        return queryset


class AccountTypeCreate(ModelMixin, LoginRequiredMixin,SuccessUrlMixin,FormMixin, CreateView):
    model = AccountType
    form_class = AccountTypeForm

    def form_valid(self,form):
        form.instance.profile = self.request.user.profile
        form.save()
        return super().form_valid(form)


class AccountTypeUpdate(ModelMixin, LoginRequiredMixin,SuccessUrlMixin,FormMixin, UpdateView):
    model = AccountType
    form_class = AccountTypeForm

    queryset = AccountType.objects.select_related('profile')

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(profile_id=self.request.user.profile.id)
        return queryset


class AccountTypeDelete(ModelMixin, LoginRequiredMixin,SuccessUrlMixin,AjaxDeleteMixin,DeleteView):
    model = AccountType
    ajax_partial = 'partials/ajax_delete_modal.html'
    queryset = AccountType.objects.select_related('profile')

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(profile_id=self.request.user.profile.id)
        return queryset


class ProjectList(BaseListView):
    model = Project
    paginate_by = 100
    queryset = Project.objects.select_related('profile')

    def get_queryset(self):
        qs = super().get_queryset().active().filter(
            profile=self.request.user.profile)
        q = self.request.GET.get('q')
        if q and q != '':
            qs = qs.filter(name__icontains=q)
        return qs


class ProjectDetail(LoginRequiredMixin, DetailView):
    model = Project
    queryset = Project.objects.select_related('profile')

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(profile_id=self.request.user.profile.id)
        return queryset


class ProjectCreate(ModelMixin, LoginRequiredMixin,SuccessUrlMixin,FormMixin, CreateView):
    model = Project
    form_class = ProjectForm

    def form_valid(self,form):
        form.instance.profile = self.request.user.profile
        form.save()
        return super().form_valid(form)


class ProjectUpdate(ModelMixin, LoginRequiredMixin,SuccessUrlMixin,FormMixin, UpdateView):
    model = Project
    form_class = ProjectForm

    queryset = Project.objects.select_related('profile')

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(profile_id=self.request.user.profile.id)
        return queryset


class ProjectDelete(ModelMixin, LoginRequiredMixin,SuccessUrlMixin,AjaxDeleteMixin,DeleteView):
    model = Project
    ajax_partial = 'partials/ajax_delete_modal.html'
    queryset = Project.objects.select_related('profile')

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(profile_id=self.request.user.profile.id)
        return queryset


class PasswordList(BaseListView):
    model = Password
    paginate_by = 100
    queryset = Password.objects.select_related('profile', 'account_type', 'project')
    def get_queryset(self):
        queryset = super().get_queryset()
        accounttype = self.request.GET.get('accounttype')
        project = self.request.GET.get('project')
        queryset = queryset.filter(profile_id=self.request.user.profile.id)
        if accounttype:
            queryset = queryset.filter(account_type=accounttype)
        if project:
            queryset = queryset.filter(project=project)
        return queryset


class PasswordDetail(LoginRequiredMixin, DetailView):
    model = Password
    queryset = Password.objects.select_related('profile', 'account_type', 'project')

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(profile_id=self.request.user.profile.id)
        return queryset



class PasswordCreate(ModelMixin, LoginRequiredMixin,SuccessUrlMixin,FormMixin, CreateView):
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

    def form_valid(self,form):
        form.instance.profile = self.request.user.profile
        form.save()
        return super().form_valid(form)


class PasswordUpdate(ModelMixin, LoginRequiredMixin,SuccessUrlMixin,FormMixin, UpdateView):
    model = Password
    form_class = PasswordForm
    queryset = Password.objects.select_related('profile', 'account_type', 'project')

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(profile_id=self.request.user.profile.id)
        return queryset


class PasswordDelete(ModelMixin, LoginRequiredMixin,SuccessUrlMixin,AjaxDeleteMixin,DeleteView):
    model = Password
    ajax_partial = 'partials/ajax_delete_modal.html'
    queryset = Password.objects.select_related('profile', 'account_type', 'project')

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(profile_id=self.request.user.profile.id)
        return queryset
