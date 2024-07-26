from django.contrib import admin
from users import models

from django.urls import path
from django.shortcuts import redirect
from django.utils.html import format_html


class UserAdmin(admin.ModelAdmin):
    list_display = ["user_id", "username", "current_plan", "updated_at"]
    list_filter = ["current_plan"]
    search_fields = ['user_id', "username", "first_name"]



class UserPlanAdmin(admin.ModelAdmin):
    list_display = ["title", "amount", "telegram_link"]
    
    change_form_template = "admin/change_form.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:object_id>/duplicate/', self.admin_site.admin_view(self.duplicate_object), name='userplan-duplicate'),
        ]
        return custom_urls + urls

    def duplicate_object(self, request, object_id):
        original_object = self.get_object(request, object_id)
        if original_object:
            new_object = original_object
            new_object.pk = None  # Set pk to None to create a new instance
            new_object.save()
            self.message_user(request, "Object duplicated successfully.")
            return redirect(f"../../{new_object.pk}/change/")
        return redirect('../../')



class UserPaymentAdmin(admin.ModelAdmin):
    list_display = ["user", "plan", "screenshoot", "updated_at", "is_verified"]
    list_filter = ["is_verified", "plan"]


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Plan, UserPlanAdmin)
admin.site.register(models.UserPayment, UserPaymentAdmin)
