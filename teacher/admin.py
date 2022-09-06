from django.contrib import admin
from .models import Cloudinfra, Router, Server, Teacher, Network

class CloudinfraInLineAdmin(admin.TabularInline):
    model = Cloudinfra

class RouterInLineAdmin(admin.TabularInline):
    model = Router

class NetworkInLineAdmin(admin.TabularInline):
    model = Network

class ServerkInLineAdmin(admin.TabularInline):
    model = Server

class TeacherAdmin(admin.ModelAdmin):
    inlines = [CloudinfraInLineAdmin]

class CloudinfraAdmin(admin.ModelAdmin):
    inlines = [RouterInLineAdmin, NetworkInLineAdmin, ServerkInLineAdmin] 

admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Cloudinfra, CloudinfraAdmin)