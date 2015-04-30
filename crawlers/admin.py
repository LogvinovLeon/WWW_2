from django.contrib import admin

from crawlers.models import Voivodeship, Powiat, Gmina, Constituency


class ConstituencyAdmin(admin.ModelAdmin):
    pass


class ConstituencyInline(admin.StackedInline):
    model = Constituency
    show_change_link = True


class GminaAdmin(admin.ModelAdmin):
    inlines = [ConstituencyInline]


class GminaInline(admin.StackedInline):
    model = Gmina
    show_change_link = True


class PowiatAdmin(admin.ModelAdmin):
    inlines = [GminaInline]


class PowiatInline(admin.StackedInline):
    model = Powiat
    show_change_link = True


class VoivodeshipAdmin(admin.ModelAdmin):
    inlines = [PowiatInline]


admin.site.register(Voivodeship, VoivodeshipAdmin)
admin.site.register(Powiat, PowiatAdmin)
admin.site.register(Gmina, GminaAdmin)
admin.site.register(Constituency, ConstituencyAdmin)
