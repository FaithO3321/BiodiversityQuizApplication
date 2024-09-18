from django.contrib import admin
from .models import Category, Quiz, Question, Choice, QuizResult

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4

class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 5

class QuizAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]

admin.site.register(Category)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(QuizResult)
