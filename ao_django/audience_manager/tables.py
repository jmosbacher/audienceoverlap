import django_tables2 as tables
from django_tables2.export.views import ExportMixin
from django.urls import reverse
from django.utils.safestring import mark_safe
from . import models


class AccountTable(ExportMixin, tables.Table):
    class Meta:
        model = models.Account
        template_name = 'django_tables2/bootstrap-responsive.html'
    # edit = tables.LinkColumn('edit', text='Edit',args=['pk'], orderable=False, empty_values=())
    export_formats = ['csv', 'xlsx','json', 'yml']

    def render_id(self, record):
        return mark_safe(f"<a href={record.pk}/edit>{record.pk}</a>")
        # return mark_safe('<a href='+reverse("Edit", args=[record.pk])+'>Edit</a>')

class AudienceTable(ExportMixin, tables.Table):
    class Meta:
        model = models.Audience
        template_name = 'django_tables2/bootstrap-responsive.html'
    # edit = tables.LinkColumn('edit', text='Edit',args=['pk'], orderable=False, empty_values=())
    export_formats = ['csv', 'xlsx','json', 'yml']

    def render_id(self, record):
        return mark_safe(f"<a href={record.pk}/edit>{record.pk}</a>")
        # return mark_safe('<a href='+reverse("Edit", args=[record.pk])+'>Edit</a>')

class OverlapTable(ExportMixin, tables.Table):
    class Meta:
        model = models.Overlap
        template_name = 'django_tables2/bootstrap-responsive.html'
    # edit = tables.LinkColumn('edit', text='Edit',args=['pk'], orderable=False, empty_values=())
    export_formats = ['csv', 'xlsx','json', 'yml']

    def render_id(self, record):
        return mark_safe(f"<a href={record.pk}/edit>{record.pk}</a>")
        # return mark_safe('<a href='+reverse("Edit", args=[record.pk])+'>Edit</a>')

class VideoTable(ExportMixin, tables.Table):
    class Meta:
        model = models.Video
        template_name = 'django_tables2/bootstrap-responsive.html'
    # edit = tables.LinkColumn('edit', text='Edit',args=['pk'], orderable=False, empty_values=())
    export_formats = ['csv', 'xlsx','json', 'yml']

    def render_id(self, record):
        return mark_safe(f"<a href={record.pk}/edit>{record.pk}</a>")
        # return mark_safe('<a href='+reverse("Edit", args=[record.pk])+'>Edit</a>')