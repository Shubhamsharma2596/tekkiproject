from django.contrib import admin
from .models import *


admin.site.register(Task)
admin.site.register(Comment)
admin.site.register(MyUser)
admin.site.register(Member)