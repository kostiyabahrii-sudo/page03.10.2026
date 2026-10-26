from django.contrib import admin
from .models import Subscriber


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ("email", "heard_from", "heard_from_other", "created_at")
    list_filter = ("heard_from",)
    search_fields = ("email", "heard_from_other")
    ordering = ("-created_at",)
