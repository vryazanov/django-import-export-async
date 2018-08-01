import uuid

from celery import shared_task
from django.contrib import admin

import import_export_async.models


@shared_task
def generate_report_by_pk(pk):
    report = import_export_async.models.Report.objects.get(pk=pk)
    model = report.content_type.model_class()

    admin_class = admin.site._registry[model]
    admin_instance = admin_class()

    formats = admin_instance.get_export_formats()
    file_format = formats[report.export_format]()

    export_data = admin_instance.get_export_data(
        file_format, model.objects.all())

    report.report.save(
        name=f'test.{file_format.get_extension()}',
        content=export_data)