from gate.models import *
from django.contrib import admin


class KeyInline(admin.TabularInline):
    model = Key

class DoorUserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'active')

    inlines = [
        KeyInline,
    ]

admin.site.register(DoorUser, DoorUserAdmin)

admin.site.register(Key)
admin.site.register(Access)
admin.site.register(FailedAccessAttempt)
