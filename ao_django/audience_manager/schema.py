import graphene

from graphene_django.types import DjangoObjectType

from .models import Account


class AccountType(DjangoObjectType):
    class Meta:
        model = Account

class Query:
    all_accounts = graphene.List(AccountType)
  
    def resolve_all_accounts(self, info, **kwargs):
        return Account.objects.all()
