from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from import_export.admin import ExportMixin as ExportClass


class ReportManager(models.Manager):
    def create(self, queryset, export_format):
        return super().create(
            export_format=export_format,
            content_type=ContentType.objects.get_for_model(queryset.model),
        )


class Report(models.Model):
    export_format = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType)

    report = models.FileField(upload_to='reports/')

    objects = ReportManager()
