from django.contrib import admin
from .models import Blog, Category

# Register your models here.
class BlogAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'category', 'list_date', 'views', 'is_published', ]
    list_display_links = ['title', ]
    list_filter = ['category', 'views', 'list_date']
    search_fields = ['title']
    list_per_page = 50
    exclude= ['views', 'slug']

admin.site.register(Blog, BlogAdmin)
admin.site.register(Category)
