import csv, io
from django.shortcuts import render
from django.contrib import messages

# Create your views here.
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")