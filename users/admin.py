from django.contrib import admin
from users import models


class UserAdmin(admin.ModelAdmin):
    list_display = ["user_id", "username", "current_plan", "updated_at"]


class UserPlanAdmin(admin.ModelAdmin):
    list_display = ["title", "amount", "telegram_link"]


class UserPaymentAdmin(admin.ModelAdmin):
    list_display = ["user", "plan", "screenshoot", "updated_at", "is_verified"]


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Plan, UserPlanAdmin)
admin.site.register(models.UserPayment, UserPaymentAdmin)
