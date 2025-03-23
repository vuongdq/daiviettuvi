from django.urls import path
from . import views

app_name = 'lasotuvi_django'

urlpatterns = [
    path('', views.home, name='home'),
    path('news/', views.NewsList.as_view(), name='news_list'),
    path('news/<slug:slug>/', views.NewsDetail.as_view(), name='news_detail'),
    path('courses/', views.CourseList.as_view(), name='course_list'),
    path('courses/<slug:slug>/', views.CourseDetail.as_view(), name='course_detail'),
    path('categories/', views.CategoryList.as_view(), name='category_list'),
    path('categories/<slug:slug>/', views.CategoryDetail.as_view(), name='category_detail'),
]