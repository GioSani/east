from django.contrib import admin

# Register your models here.
from .models import User,UserToken


# class SuperUser(UserAdmin):
#     ordering = ['id']


admin.site.register(User)

admin.site.register(UserToken) 