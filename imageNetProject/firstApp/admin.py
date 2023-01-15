from django.contrib import admin

# Register your models here.
from .models import * 

admin.site.register(Users)
admin.site.register(Photo)
admin.site.register(Photo_Details)
admin.site.register(Photo_History)