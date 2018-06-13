from django.contrib import admin

from .models import Jedi, Planet, Question, Order

# Register your models here.
admin.site.register(Jedi)
admin.site.register(Planet)
admin.site.register(Question)
admin.site.register(Order)
