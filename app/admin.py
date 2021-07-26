from django.contrib import admin
from .models import *

admin.site.register(kanji)
admin.site.register(vocab)
admin.site.register(meanings)
admin.site.register(readings)
admin.site.register(source)
admin.site.register(examples)
admin.site.register(user_synonyms)
