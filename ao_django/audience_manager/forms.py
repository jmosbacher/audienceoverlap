from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field
from . import models
# from table_select_widget import TableSelectMultiple


class AccountForm(forms.ModelForm):
    class Meta:
        model = models.Account
        fields = ('id', 'name', 'access_token')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        # self.helper.form_class = 'form-inline'
        self.helper.form_method = 'post'
        # self.helper.field_class = 'col-sm-6'
        self.helper.layout = Layout(
                Field('id',readonly=True),
      'name','access_token',
    )
        self.helper.add_input(Submit('submit', 'Save'))



class SelectAccountsForm(forms.Form):
    accounts = forms.ModelMultipleChoiceField(
        queryset=models.Account.objects.all().values_list('name', flat=True),
        widget=forms.CheckboxSelectMultiple(
            # choices=[(item.id, item.name) for item in models.Account.objects.all()]
        )
        
    )

class VideoForm(forms.ModelForm):
    class Meta:
        model = models.Video
        fields = ('id', 'account', 'link', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        # self.helper.form_class = 'form-inline'
        self.helper.form_method = 'post'
        # self.helper.field_class = 'col-sm-6'
        self.helper.layout = Layout(
                Field('id',readonly=True),
       'account', 'link',
    )
        self.helper.add_input(Submit('submit', 'Save'))


class AudienceForm(forms.ModelForm):
    class Meta:
        model = models.Audience
        fields = ('id', 'name', 'account', 'size')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        # self.helper.form_class = 'form-inline'
        self.helper.form_method = 'post'
        # self.helper.field_class = 'col-sm-6'
        self.helper.layout = Layout(
                Field('id',readonly=True),
      'name', 'account', 'size'
    )
        self.helper.add_input(Submit('submit', 'Save'))



class OverlapForm(forms.ModelForm):
    class Meta:
        model = models.Overlap
        fields = ('id', 'account', 'audience_1', 'audience_2', 'overlap')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        # self.helper.form_class = 'form-inline'
        self.helper.form_method = 'post'
        # self.helper.field_class = 'col-sm-6'
        self.helper.layout = Layout(
                Field('id',readonly=True),
       'account', 'audience_1', 'audience_2', 'overlap'
    )
        self.helper.add_input(Submit('submit', 'Save'))




