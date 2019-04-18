import uuid

from celery import shared_task
from django.contrib import admin
from django.core.files.base import ContentFile

import import_export_async.models


@shared_task
def generate_report_by_pk(pk):
    report = import_export_async.models.Report.objects.get(pk=pk)
    report.commit_status(report.STARTED)

    try:

        model = report.content_type.model_class()

        admin_class = admin.site._registry[model]

        formats = admin_class.get_export_formats()
        file_format = formats[report.export_format]()

        report.commit_status(report.EXPORTING)
        export_data = admin_class.get_export_data(
            file_format, model.objects.all(), request=None)

        if not isinstance(export_data, bytes):
            report.commit_status(report.ENCODING)
            export_data = export_data.encode('utf-8')

        name =\
            f'{model._meta.app_label}-{model._meta.model_name}-{uuid.uuid4()}'

        report.commit_status(report.SAVING)
        report.report.save(
            name=f'{name}.{file_format.get_extension()}',
            content=ContentFile(export_data), save=False)
    except Exception as e:
        report.failed_on = report.status
        report.commit_status(report.ERROR)
        raise
    else:
        report.commit_status(report.PROCESSED)
