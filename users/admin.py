from django.contrib import admin
from users import models

from django.urls import path
from django.shortcuts import redirect

from import_export.admin import ExportActionModelAdmin
from import_export import resources
from import_export.formats.base_formats import XLS, XLSX, JSON


class UserResource(resources.ModelResource):
    class Meta:
        model = models.User
        fields = ("user_id", "username", "current_plan__title", "updated_at")

@admin.register(models.User)
class UserAdmin(ExportActionModelAdmin):
    resource_class = UserResource
    list_display = ["user_id", "username", "current_plan", "updated_at"]
    list_filter = ["current_plan"]
    search_fields = ['user_id', "username", "first_name"]
    list_per_page = 20
    list_select_related = ("current_plan", )


class PlanResouces(resources.ModelResource):
    class Meta:
        model = models.Plan
        fields = ("title", "amount", "telegram_link", "updated_at")

@admin.register(models.Plan)
class UserPlanAdmin(ExportActionModelAdmin):
    resource_class = PlanResouces
    list_display = ["title", "amount", "telegram_link"]
    list_per_page = 20
    
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
            new_object.pk = None
            new_object.save()
            self.message_user(request, "Object duplicated successfully.")
            return redirect(f"../../{new_object.pk}/change/")
        return redirect('../../')


class UserPaymentResource(resources.ModelResource):
    class Meta:
        model = models.UserPayment
        fields = ("user", "plan__title", "screenshoot", "is_verified", "updated_at")

@admin.register(models.UserPayment)
class UserPaymentAdmin(ExportActionModelAdmin):
    resource_class = UserPaymentResource
    list_display = ["user", "plan", "screenshoot", "updated_at", "is_verified"]
    list_filter = ["is_verified", "plan"]
    list_per_page = 20
    list_select_related = ("user", "plan", )

