from django.contrib import admin
import requests
from .models import Blog, Category
from django.core.exceptions import ValidationError

from .views import predict

from django.forms import ModelForm

class BlogAdminForm(ModelForm):
    class Meta:
        model = Blog
        fields = '__all__'

# Register your models here.
class BlogAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'category', 'list_date', 'views', 'is_published', ]
    list_display_links = ['title', ]
    list_filter = ['category', 'views', 'list_date']
    search_fields = ['title']
    list_per_page = 50
    exclude= ['views', 'slug']

    form = BlogAdminForm

    def save_model(self, request, obj, form, change):
        content = obj.content

        api_url = 'http://127.0.0.1:8000/predict/'

        try:
            req = requests.get(api_url, params={'text': content})
            if req.status_code == 200:
                if req.json().get('LR') == 'Fake News':
                    raise ValidationError("Blog validation failed. Please check your input.")
            else:
                raise ValidationError("API request failed. Please try again later.")

            # Proceed with saving the model
            super().save_model(request, obj, form, change)
        except:
            pass



    

admin.site.register(Blog, BlogAdmin)
admin.site.register(Category)
