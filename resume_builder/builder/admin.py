from django.contrib import admin
from .models import *
from .models import ContactQuery


admin.site.register(Resume)
admin.site.register(PersonalInfo)
admin.site.register(Education)
admin.site.register(Experience)
admin.site.register(Skill)
admin.site.register(Project)
admin.site.register(ContactQuery)
