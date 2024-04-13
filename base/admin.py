from django.contrib import admin
from base.models import Statements, Transaction, UssdRequest, UssdState, UssdResponse,Profile

# Register your models here.

@admin.register(UssdRequest)
class UssdRequestAdmin(admin.ModelAdmin):
    list_display = tuple(field.name for field in UssdRequest._meta.fields)
    search_fields = ["sessionId", "msisdn"]


@admin.register(UssdResponse)
class UssdResponseAdmin(admin.ModelAdmin):
    list_display = tuple(field.name for field in UssdResponse._meta.fields)
    search_fields = ["sessionId", "msisdn"]


@admin.register(UssdState)
class UssdStateAdmin(admin.ModelAdmin):
    list_display = tuple(field.name for field in UssdState._meta.fields)
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