from django.shortcuts import render
from django.views import generic

# tutorial/views.py
from django.shortcuts import render
from django_tables2 import SingleTableView
from django_tables2.export.views import ExportMixin
from datatableview.views import XEditableDatatableView
from datatableview import helpers
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, Group
from ..models import Account

from rest_framework import viewsets
from .serializers import UserSerializer, GroupSerializer, AccountSerializer


class UserViewSet(LoginRequiredMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class AccountViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows accounts to be viewed or edited.
    """
    queryset = Account.objects.all()
    serializer_class = AccountSerializer





