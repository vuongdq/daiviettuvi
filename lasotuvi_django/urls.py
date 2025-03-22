from django.urls import path
from lasotuvi_django.views import api, lasotuvi_django_index

urlpatterns = [
    path('api/', api),           # Thay url(r'^api') bằng path('api/')
    path('', lasotuvi_django_index)  # Thay url(r'^$') bằng path('')
]