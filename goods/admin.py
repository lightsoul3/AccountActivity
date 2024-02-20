from django.contrib import admin
from .models import Category, Good

# Registered my mmodels in admin
admin.site.register(Category)
admin.site.register(Good)
