import csv, io
from django.contrib import admin, messages
from django import forms
from django.urls import path
from django.shortcuts import render, redirect
from import_export.admin import ImportExportModelAdmin

# Register your models here.

from .models import Candidato

@admin.register(Candidato)
class CandidatoAdmin(ImportExportModelAdmin):
    list_display = ['nome', 'email', 'cpf']
    ordering = ['nome']
