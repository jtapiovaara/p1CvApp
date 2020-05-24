from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.utils.translation import gettext_lazy as _

from .models import Projekti


class ProjektiAdmin(admin.ModelAdmin):
    list_display = ['title', 'projtype']
    list_filter = ('projtype',)
    radio_fields = {'projtype': admin.HORIZONTAL}
    search_fields = ['title', 'description']



class FlatPageAdmin(FlatPageAdmin):
    fieldsets = (
        (None, {'fields': ('url', 'title', 'content', 'sites')}),
        (_('Advanced options'), {
            'classes': ('collapse',),
            'fields': (
                'enable_comments',
                'registration_required',
                'template_name',
            ),
        }),
    )


admin.site.register(Projekti, ProjektiAdmin)
admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)
