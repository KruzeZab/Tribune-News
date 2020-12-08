from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.db.models import F

from .models import Blog

# Create your views here.
class IndexView(ListView):
    context_object_name = 'blogs'
    template_name = 'blog/index.html'

    def get_queryset(self):
        return Blog.objects.filter(is_published=True).only('title', 'category', 'photo_main', 'list_date', 'description', 'slug')[:25]
        

class CategoryView(ListView):
    template_name = 'blog/category.html'
    context_object_name = 'blogs'

    def get_queryset(self):
        cat = self.kwargs.get('cat')
        blog = Blog.objects.filter(is_published=True).filter(category__name=cat).only('title', 'category', 'photo_main', 'list_date', 'description', 'slug')[:25]
        return get_list_or_404(blog)

    

def articleView(request, category, slug):
    article = get_object_or_404(Blog, slug=slug)
    Blog.objects.filter(slug=slug).update(views=F('views')+1)
    context = {}
    context['articles'] = Blog.objects.filter(is_published=True).order_by('-list_date').only('title', 'photo_main', 'slug')[:12]
    context['blog'] = article
    return render(request, 'blog/article.html', context)







class SearchView(ListView):
    template_name = 'blog/search.html'
    context_object_name = 'blogs'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        return Blog.objects.filter(is_published=True).filter(title__icontains=query)
    







def showContent(request):
    #Get length of queryset
    if request.is_ajax():
        count = Blog.objects.filter(is_published=True).count()
        print(count)
        context = {}
        start = int(request.GET.get('start'))
        end = int(request.GET.get('end'))
        
        posts = Blog.objects.filter(is_published=True).only('title', 'category', 'description', 'list_date', 'photo_main', 'slug')[start:end+1]
        
        context['last'] = False
        if start>count:
            context['last'] = True
        context['posts'] = posts
        return render(request, 'blog/data.html', context)
    #return HttpResponse('Hello World')

def catShowContent(request):
    if request.is_ajax():
        cat = request.GET.get('cat')
        start = int(request.GET.get('start'))
        end = int(request.GET.get('end'))
        count = Blog.objects.filter(is_published=True).filter(category__name=cat).count()

        context = {}
        posts = Blog.objects.filter(is_published=True).filter(category__name=cat).only('title', 'category', 'description', 'list_date', 'photo_main', 'slug')[start:end+1]
        
        context['last'] = False
        if start>count:
            context['last'] = True
        context['posts'] = posts
        return render(request, 'blog/data.html', context)
        
        



