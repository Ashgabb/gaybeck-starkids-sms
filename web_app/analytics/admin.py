from django.contrib import admin
from .models import AnalyticsReport

@admin.register(AnalyticsReport)
class AnalyticsReportAdmin(admin.ModelAdmin):
    list_display = ('report_type', 'title', 'generated_at')
    list_filter = ('report_type', 'generated_at')
    readonly_fields = ('generated_at',)
