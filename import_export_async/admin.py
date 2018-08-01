from django.contrib import admin as django_admin
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from import_export import admin

import import_export_async.models
import import_export_async.tasks


class AsyncExportMixin(admin.ExportActionModelAdmin):
    def has_export_permission(self, *args, **kwargs):
        return True

    def export_admin_action(self, request, queryset):
        """
        Exports the selected rows using file_format.
        """
        export_format = request.POST.get('file_format')

        if not export_format:
            messages.warning(request, _('You must select an export format.'))
        else:
            report = import_export_async.models.Report.objects.create(
                queryset, export_format)
            import_export_async.tasks.generate_report_by_pk.delay(report.pk)
            return redirect('/admin')

    export_admin_action.short_description = _(
        'Export selected %(verbose_name_plural)s')

    actions = [export_admin_action]


django_admin.site.register(import_export_async.models.Report)
