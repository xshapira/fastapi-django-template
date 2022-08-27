from django.contrib import admin

from posts import models


@admin.register(models.Programmer)
class ProgrammerAdmin(admin.ModelAdmin):
    pass


# @admin.register(models.Programmer)
# class ProgrammerAdmin(admin.ModelAdmin):
#     list_display = (
#         "name",
#         "age",
#         "gender",
#         "languages",
#     )

#     search_fields = ("name",)

#     filter_horizontal = ("gender",)
