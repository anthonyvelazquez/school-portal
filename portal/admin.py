from django.contrib import admin

from .models import Exam, Question, StudentReport

admin.site.register(Exam)
admin.site.register(Question)
admin.site.register(StudentReport)