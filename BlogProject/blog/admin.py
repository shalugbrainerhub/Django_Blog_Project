from django.contrib import admin


from .models import *

admin.site.register(UserRegistration)
admin.site.register(Post)
admin.site.register(Comment)
