import datetime
import json

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from lasotuvi.DiaBan import diaBan
from lasotuvi.ThienBan import lapThienBan
from django.core.paginator import Paginator

from lasotuvi_django.utils import lapDiaBan
from .models import Category, News, Course, Tag


def api(request):
    now = datetime.datetime.now()
    hoTen = (request.GET.get('hoten'))
    ngaySinh = int(request.GET.get('ngaysinh', now.day))
    thangSinh = int(request.GET.get('thangsinh', now.month))
    namSinh = int(request.GET.get('namsinh', now.year))
    gioiTinh = 1 if request.GET.get('gioitinh') == 'nam' else -1
    gioSinh = int(request.GET.get('giosinh', 1))
    timeZone = int(request.GET.get('muigio', 7))
    duongLich = False if request.GET.get('amlich') == 'on' else True
    db = lapDiaBan(diaBan, ngaySinh, thangSinh, namSinh, gioSinh,
                   gioiTinh, duongLich, timeZone)
    thienBan = lapThienBan(ngaySinh, thangSinh, namSinh,
                           gioSinh, gioiTinh, hoTen, db)
    laso = {
        'thienBan': thienBan,
        'thapNhiCung': db.thapNhiCung
    }
    my_return = (json.dumps(laso, default=lambda o: o.__dict__))
    return HttpResponse(my_return, content_type="application/json")


def lasotuvi_django_index(request):
    return render(request, 'lasotuvi_django/index.html')

def home(request):
    featured_news = News.objects.filter(is_published=True, is_featured=True)[:6]
    featured_courses = Course.objects.filter(is_published=True, is_featured=True)[:6]
    categories = Category.objects.filter(is_active=True, parent=None)[:10]
    latest_news = News.objects.filter(is_published=True, is_featured=False)[:6]
    latest_courses = Course.objects.filter(is_published=True, is_featured=False)[:6]
    
    context = {
        'featured_news': featured_news,
        'featured_courses': featured_courses,
        'categories': categories,
        'latest_news': latest_news,
        'latest_courses': latest_courses,
    }
    return render(request, 'lasotuvi_django/home.html', context)

class NewsList(ListView):
    model = News
    template_name = 'lasotuvi_django/news_list.html'
    context_object_name = 'news_list'
    paginate_by = 12

    def get_queryset(self):
        return News.objects.filter(is_published=True).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_active=True)
        return context

class NewsDetail(DetailView):
    model = News
    template_name = 'lasotuvi_django/news_detail.html'
    context_object_name = 'news'
    slug_url_kwarg = 'slug'

    def get_object(self):
        obj = super().get_object()
        obj.views_count += 1
        obj.save()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_news'] = self.object.related_news.filter(is_published=True)[:3]
        context['categories'] = Category.objects.filter(is_active=True)
        context['featured_news'] = News.objects.filter(is_published=True, is_featured=True)[:5]
        return context

class CourseList(ListView):
    model = Course
    template_name = 'lasotuvi_django/course_list.html'
    context_object_name = 'course_list'
    paginate_by = 12

    def get_queryset(self):
        return Course.objects.filter(is_published=True).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_active=True)
        return context

class CourseDetail(DetailView):
    model = Course
    template_name = 'lasotuvi_django/course_detail.html'
    context_object_name = 'course'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lessons'] = self.object.lessons.all().order_by('order')
        context['categories'] = Category.objects.filter(is_active=True)
        return context

class CategoryList(ListView):
    model = Category
    template_name = 'lasotuvi_django/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.filter(is_active=True, parent=None)

class CategoryDetail(DetailView):
    model = Category
    template_name = 'lasotuvi_django/category_detail.html'
    context_object_name = 'category'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get featured and latest news from this category
        context['featured_news'] = News.objects.filter(
            category=self.object,
            is_published=True,
            is_featured=True
        ).order_by('-created_at')[:3]
        
        context['latest_news'] = News.objects.filter(
            category=self.object,
            is_published=True,
            is_featured=False
        ).order_by('-created_at')[:6]
        
        # Get featured and latest courses from this category
        context['featured_courses'] = Course.objects.filter(
            category=self.object,
            is_published=True,
            is_featured=True
        ).order_by('-created_at')[:3]
        
        context['latest_courses'] = Course.objects.filter(
            category=self.object,
            is_published=True,
            is_featured=False
        ).order_by('-created_at')[:6]
        
        context['categories'] = Category.objects.filter(is_active=True)
        return context

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    
    # Get featured and latest news from this category
    featured_news = News.objects.filter(
        category=category,
        is_published=True,
        is_featured=True
    ).order_by('-created_at')[:3]
    
    latest_news = News.objects.filter(
        category=category,
        is_published=True,
        is_featured=False
    ).order_by('-created_at')[:6]
    
    # Get featured and latest courses from this category
    featured_courses = Course.objects.filter(
        category=category,
        is_published=True,
        is_featured=True
    ).order_by('-created_at')[:3]
    
    latest_courses = Course.objects.filter(
        category=category,
        is_published=True,
        is_featured=False
    ).order_by('-created_at')[:6]
    
    context = {
        'category': category,
        'featured_news': featured_news,
        'latest_news': latest_news,
        'featured_courses': featured_courses,
        'latest_courses': latest_courses,
    }
    
    return render(request, 'lasotuvi_django/category_detail.html', context)

def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug)
    
    # Get lessons ordered by their order field
    lessons = course.lessons.all().order_by('order')
    
    # Get related courses from the same category
    related_courses = Course.objects.filter(
        category=course.category,
        is_published=True
    ).exclude(id=course.id)[:3]
    
    context = {
        'course': course,
        'lessons': lessons,
        'related_courses': related_courses,
    }
    
    return render(request, 'lasotuvi_django/course_detail.html', context)
