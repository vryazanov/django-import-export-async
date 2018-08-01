from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models
from import_export.admin import ExportMixin as ExportClass


class ReportManager(models.Manager):
    def create(self, queryset, export_format):
        return super().create(
            export_format=export_format,
            content_type=ContentType.objects.get_for_model(queryset.model),
        )


class Report(models.Model):
    WAITING = 'WAITING'
    PROCESSED = 'PROCESSED'

    STATUS_CHOICES = (
        (WAITING, 'Waiting'),
        (PROCESSED, 'Processed'),
    )

    status = models.CharField(
        choices=STATUS_CHOICES, default=WAITING, max_length=32)
    export_format = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType)

    report = models.FileField(upload_to='async_reports/')
    created = models.DateTimeField(auto_now_add=True)

    objects = ReportManager()

    def __str__(self):
        return str(self.content_type)

    def get_admin_url(self):
        return reverse('admin:import_export_async_report_change', 
                       args=(self.pk,))
