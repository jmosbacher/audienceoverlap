from django.shortcuts import render

from django.views import generic
# tutorial/views.py
from django.shortcuts import render
from django_tables2 import SingleTableView
from django_tables2.export.views import ExportMixin
# from datatableview.views import XEditableDatatableView
from datatableview import helpers
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required


# from django.contrib.auth.models import User, Group
from . import models
from . import tables
from . import forms

from ao_django import settings

from rest_framework import viewsets
from bokeh.embed import server_session
from bokeh.util import session_id
import os

BOKEH_KEY=os.environ.get('BOKEH_SECRET_KEY')
BOKEH_ADDRESS=os.environ.get('BOKEH_ADDRESS', "http://localhost:5006/audienceoverlap")

def bokeh_js_script(relative_urls=True):
    #session = pull_session(self.address)
    #session.document.template_variables['data_path'] = self.data_path
    s_id = session_id.generate_session_id(secret_key=BOKEH_KEY, signed=True)
    return server_session(None,session_id=s_id, url=BOKEH_ADDRESS,
                            relative_urls=relative_urls,
                            resources='default')

def csrf_failure(request, reason=""):
    ctx = {'message': 'some custom messages'}
    return render('audience_manager/403.html', ctx)

def home(request):
    return render(request, 'audience_manager/home.html')

@login_required
@permission_required('overlaps.can_view', raise_exception=True)
def visualizations(request):
    ctx = {"bokeh_script": bokeh_js_script()}
    return render(request, 'audience_manager/visualizations.html', context=ctx)


class AccountCreateView(PermissionRequiredMixin, generic.CreateView):
    model = models.Account
    template_name = 'audience_manager/form.html'
    fields = ('id','name', 'access_token')
    permission_required = 'accounts.can_create'


class AccountUpdateView(PermissionRequiredMixin, generic.UpdateView):
    model = models.Account
    form_class = forms.AccountForm
    template_name = 'audience_manager/form.html'
    permission_required = 'accounts.can_update'

class AccountsTableView(PermissionRequiredMixin, ExportMixin, SingleTableView):
    table_class = tables.AccountTable
    model = models.Account
    export_name = 'accounts'
    template_name = 'audience_manager/table.html'
    permission_required = 'accounts.can_view'

    def get_queryset(self):
        return models.Account.objects.all()

    def get_permission_denied_message(self):
        return 'You do not have access to this content.'
        
class SelectAccountsView(PermissionRequiredMixin, generic.FormView):
    template_name = 'audience_manager/form.html'
    form_class = forms.SelectAccountsForm
    success_url = ''
    permission_required = 'overlaps.can_create'

    def get_queryset(self):
        return models.Account.objects.all()