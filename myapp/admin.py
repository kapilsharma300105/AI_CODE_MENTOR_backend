from django.contrib import admin
from .models import CodeHistory, ChatHistory, Practice, Performance

admin.site.register(CodeHistory)
admin.site.register(ChatHistory)
admin.site.register(Practice)
admin.site.register(Performance)