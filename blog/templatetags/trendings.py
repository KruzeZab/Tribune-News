from django.utils.http import urlencode
from django import template
from blog.models import Blog

register = template.Library()

@register.inclusion_tag('partials/_trendings.html')
def show_trendings(num=6):
    trendings = Blog.objects.filter(is_published=True).order_by('-views').only('title', 'category', 'photo_main', 'list_date', 'description', 'slug')[:num]
    return {'trendings': trendings}

@register.inclusion_tag('partials/_trending_title.html')
def show_trending_list(num=5):
    trending_titles = Blog.objects.filter(is_published=True).order_by('-views').values('title', 'category', 'slug')[:num]
    return {'trendings': trending_titles}


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    query = context['request'].GET.dict()
    query.update(kwargs)
    return urlencode(query)



