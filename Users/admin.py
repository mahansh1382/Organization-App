from django.contrib import admin

from Users.models import Authentication, Users
@admin.register(Authentication)
class AdminAuthentication(admin.ModelAdmin):
    pass


@admin.register(Users)
class AdminUser(admin.ModelAdmin):
    list_display=['last_name']
    