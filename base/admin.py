from django.contrib import admin
from base.models import (
    Statements,
    Transaction,
    UssdLog,
    UssdScreen,
    UssdSession,
    Profile,
)

# Register your models here.


@admin.register(UssdLog)
class UssdLogAdmin(admin.ModelAdmin):
    list_display = tuple(field.name for field in UssdLog._meta.fields)
    search_fields = ["sessionId", "msisdn"]


@admin.register(UssdSession)
class UssdSessionAdmin(admin.ModelAdmin):
    list_display = tuple(field.name for field in UssdSession._meta.fields)
    search_fields = ["sessionId", "msisdn"]


@admin.register(UssdScreen)
class UssdScreenAdmin(admin.ModelAdmin):
    list_display = tuple(field.name for field in UssdScreen._meta.fields)
    search_fields = ["sessionId", "msisdn"]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = tuple(field.name for field in Profile._meta.fields)
    search_fields = ["full_name", "email"]


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = tuple(field.name for field in Transaction._meta.fields)
    search_fields = ["profile__full_name", "profile__email"]


@admin.register(Statements)
class StatementsAdmin(admin.ModelAdmin):
    list_display = tuple(field.name for field in Statements._meta.fields)
    search_fields = ["profile__full_name", "profile__email"]
