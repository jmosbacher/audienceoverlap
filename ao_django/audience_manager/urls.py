from django.urls import path
from django.conf.urls import url, include
from . import views
from django.views.defaults import permission_denied
from django.utils.functional import curry

handler403 = curry(permission_denied, template_name='audience_manager/403.html')


urlpatterns = [
    path('', views.home, name='audience_manager'),
    path('accounts/', views.AccountsTableView.as_view(), name='accounts'),
path('accounts/signup/', views.AccountsTableView.as_view(), name='accounts'),
    path('accounts/select/', views.SelectAccountsView.as_view(), name='select_accounts'),
    path('accounts/add/', views.AccountCreateView.as_view(), name='add_account'),
    path('accounts/<int:pk>/edit/', views.AccountUpdateView.as_view(), name='edit_account'),

    path('audiences/', views.AccountsTableView.as_view(), name='audiences'),
    path('overlaps/', views.AccountsTableView.as_view(), name='overlaps'),
    path('videos/', views.AccountsTableView.as_view(), name='videos'),
    path('visualizations', views.visualizations, name='visualizations'),
    path('api/', include('audience_manager.api.urls'), name='api'),
]