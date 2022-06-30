from django.contrib import admin
from .models import Articles,Like,Users


# Register your models here.
admin.site.register(Articles)
admin.site.register(Like)
admin.site.register(Users)
