from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Translation

class TranslationResource(resources.ModelResource):
    class Meta:
        model = Translation
        fields = ('id', 'english', 'turkmen')
        import_id_fields = ['english']
        skip_unchanged = True
        report_skipped = True

@admin.register(Translation)
class TranslationAdmin(ImportExportModelAdmin):
    resource_class = TranslationResource
    list_display = ('english', 'turkmen')
    search_fields = ('english', 'turkmen')
    ordering = ['english']  # 👈 ensures admin list is ordered A→Z
