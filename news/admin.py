from django.contrib import admin

from news.models import NewsComment, NewsImage, News, NewsVideo

admin.site.register(News)
admin.site.register(NewsImage)
admin.site.register(NewsVideo)
admin.site.register(NewsComment)
