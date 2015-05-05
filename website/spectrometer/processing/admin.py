from django.contrib import admin

# Register your models here.
from processing.models import Choice, Question, SpectralImage

class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]

class DocumentText(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields': ['source']}),
	]

admin.site.register(Question, QuestionAdmin)
admin.site.register(SpectralImage)