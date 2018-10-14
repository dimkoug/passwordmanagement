from django.urls import path

from .views import (
    AccountTypeList, AccountTypeDetail, AccountTypeCreate, AccountTypeUpdate,
    AccountTypeDelete, ProjectList, ProjectDetail, ProjectCreate,
    ProjectUpdate, ProjectDelete, PasswordList, PasswordDetail, PasswordCreate,
    PasswordUpdate, PasswordDelete
)


urlpatterns = [
    path('', ProjectList.as_view(), name='project-list'),
    path('<int:pk>/', ProjectDetail.as_view(),
         name='project-detail'),
    path('create/', ProjectCreate.as_view(),
         name='project-create'),
    path('<int:pk>/update/', ProjectUpdate.as_view(),
         name='project-update'),
    path('<int:pk>/delete', ProjectDelete.as_view(),
         name='project-delete'),

    path('accounttype/', AccountTypeList.as_view(), name='accounttype-list'),
    path('accounttype/<int:pk>/', AccountTypeDetail.as_view(),
         name='accounttype-detail'),
    path('accounttype/create/', AccountTypeCreate.as_view(),
         name='accounttype-create'),
    path('accounttype/<int:pk>/update/', AccountTypeUpdate.as_view(),
         name='accounttype-update'),
    path('accounttype/<int:pk>/delete', AccountTypeDelete.as_view(),
         name='accounttype-delete'),

    path('password/', PasswordList.as_view(), name='password-list'),
    path('password/<int:pk>/', PasswordDetail.as_view(),
         name='password-detail'),
    path('password/create/', PasswordCreate.as_view(),
         name='password-create'),
    path('password/<int:pk>/update/', PasswordUpdate.as_view(),
         name='password-update'),
    path('password/<int:pk>/delete', PasswordDelete.as_view(),
         name='password-delete'),

]
