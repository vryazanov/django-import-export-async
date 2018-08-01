from django.contrib import admin as django_admin

from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.utils.translation import ugettext_lazy as _
from import_export import admin, forms

import import_export_async.models
import import_export_async.tasks


class AsyncExportMixin(admin.ExportMixin):
    def has_export_permission(self, *args, **kwargs):
        return True

    def export_action(self, request, *args, **kwargs):
        formats = self.get_export_formats()
        form = forms.ExportForm(formats, request.POST or None)

        if form.is_valid():
            export_format = int(form.cleaned_data['file_format'])
            queryset = self.get_export_queryset(request)

            report = import_export_async.models.Report.objects.create(
                queryset, export_format)
            import_export_async.tasks.generate_report_by_pk.delay(report.pk)

            return redirect(report.get_admin_url())

        context = self.get_export_context_data()

        context.update(self.admin_site.each_context(request))

        context['title'] = _("Export")
        context['form'] = form
        context['opts'] = self.model._meta
        request.current_app = self.admin_site.name
        return TemplateResponse(request, [self.export_template_name],
                                context)

django_admin.site.register(import_export_async.models.Report)
