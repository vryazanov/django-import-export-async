from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.db import models
from import_export.admin import ExportMixin as ExportClass


class ReportManager(models.Manager):
    def create(self, queryset, export_format):
        return super().create(
            export_format=export_format,
            content_type=ContentType.objects.get_for_model(
                queryset.model,
                for_concrete_model=False,
            ),
        )


class Report(models.Model):
    WAITING = 'WAITING'
    STARTED = 'STARTED'
    EXPORTING = 'EXPORTING'
    ENCODING = 'ENCODING'
    SAVING = 'SAVING'
    PROCESSED = 'PROCESSED'
    ERROR = 'ERROR'

    STATUS_CHOICES = (
        (WAITING, 'Waiting'),
        (STARTED, 'Started'),
        (EXPORTING, 'Exporting'),
        (ENCODING, 'Encoding'),
        (SAVING, 'Saving'),
        (PROCESSED, 'Processed'),
        (ERROR, 'Error'),
    )

    status = models.CharField(
        choices=STATUS_CHOICES, default=WAITING, max_length=32)
    export_format = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    failed_on = models.CharField(
        choices=STATUS_CHOICES, null=True, blank=True, max_length=32)

    report = models.FileField(upload_to='async_reports/')
    created = models.DateTimeField(auto_now_add=True)

    objects = ReportManager()

    def __str__(self):
        return f'{self.content_type} - {self.get_status_display()}'

    def get_admin_url(self):
        return reverse('admin:import_export_async_report_change',
                       args=(self.pk,))

    def commit_status(self, status):
        self.status = status
        self.save()
