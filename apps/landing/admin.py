
from django.contrib import admin
from .models import Section, Service, SuccessCase, ContactMessage, SelfAssessment

admin.site.register(Section)
admin.site.register(Service)
admin.site.register(SuccessCase)
admin.site.register(ContactMessage)
admin.site.register(SelfAssessment)