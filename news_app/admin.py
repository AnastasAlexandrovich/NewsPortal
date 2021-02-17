from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from news_app.models import Item, User, Comment

admin.site.register(Item)
admin.site.register(User)
admin.site.register(Comment, MPTTModelAdmin)

