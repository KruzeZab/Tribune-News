from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.db.models import F
from django.http import JsonResponse
from django.http import QueryDict

import joblib
import re
import string
from django.views.decorators.csrf import csrf_exempt

from .models import Blog

def wordppt(text):
    text = text.lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub("\\W", " ", text)
    text = re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    text = re.sub('\w*\d\w*', '', text)
    return text


def output_label(n):
    if n == 0:
        return 'Fake News'
    elif n == 1:
        return 'Not A Fake News'


# You can create your views here.
class IndexView(ListView):
    context_object_name = "blogs"
    template_name = "blog/index.html"

    def get_queryset(self):
        return Blog.objects.filter(is_published=True).only(
            "title", "category", "photo_main", "list_date", "description", "slug"
        )[:25]


class CategoryView(ListView):
    template_name = "blog/category.html"
    context_object_name = "blogs"

    def get_queryset(self):
        cat = self.kwargs.get("cat")
        blog = (
            Blog.objects.filter(is_published=True)
            .filter(category__name=cat)
            .only(
                "title", "category", "photo_main", "list_date", "description", "slug"
            )[:25]
        )
        return get_list_or_404(blog)


def articleView(request, category, slug):
    article = get_object_or_404(Blog, slug=slug)
    Blog.objects.filter(slug=slug).update(views=F("views") + 1)
    context = {}
    context["articles"] = (
        Blog.objects.filter(is_published=True)
        .order_by("-list_date")
        .only("title", "photo_main", "slug")[:12]
    )
    context["blog"] = article
    return render(request, "blog/article.html", context)


class SearchView(ListView):
    template_name = "blog/search.html"
    context_object_name = "blogs"
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get("q", "")
        return Blog.objects.filter(is_published=True).filter(title__icontains=query)


def showContent(request):
    # Get length of queryset
    if request.is_ajax():
        count = Blog.objects.filter(is_published=True).count()
        print(count)
        context = {}
        start = int(request.GET.get("start"))
        end = int(request.GET.get("end"))

        posts = Blog.objects.filter(is_published=True).only(
            "title", "category", "description", "list_date", "photo_main", "slug"
        )[start : end + 1]

        context["last"] = False
        if start > count:
            context["last"] = True
        context["posts"] = posts
        return render(request, "blog/data.html", context)
    return render(request, "404.html", status=404)


def catShowContent(request):
    if request.is_ajax():
        cat = request.GET.get("cat")
        start = int(request.GET.get("start"))
        end = int(request.GET.get("end"))
        count = (
            Blog.objects.filter(is_published=True).filter(category__name=cat).count()
        )

        context = {}
        posts = (
            Blog.objects.filter(is_published=True)
            .filter(category__name=cat)
            .only(
                "title", "category", "description", "list_date", "photo_main", "slug"
            )[start : end + 1]
        )

        context["last"] = False
        if start > count:
            context["last"] = True
        context["posts"] = posts
        return render(request, "blog/data.html", context)


def fake_news(request):
    return render(request, "blog/fake-news.html")

@csrf_exempt
def predict(request):
    if request.method == 'GET':
        text = request.GET.get('text')

        LR = joblib.load('./blog/algorithm/dt.joblib')
        DT = joblib.load('./blog/algorithm/dt.joblib')
        GB = joblib.load('./blog/algorithm/gb.joblib')
        RF = joblib.load('./blog/algorithm/rf.joblib')
        vectorization = joblib.load('./blog/algorithm/vectorization.joblib')

        text_cleaned = wordppt(text)
        new_x_test = [text_cleaned]
        new_xv_test = vectorization.transform(new_x_test)

        pred_LR = LR.predict(new_xv_test)
        pred_DT = DT.predict(new_xv_test)
        pred_GB = GB.predict(new_xv_test)
        pred_RF = RF.predict(new_xv_test)

        
        return JsonResponse({
            'LR': output_label(pred_LR[0]),
            'DT': output_label(pred_DT[0]),
            'GB':  output_label(pred_GB[0]),
            'RF':  output_label(pred_RF[0])
        })
