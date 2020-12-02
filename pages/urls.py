from django.urls import path,re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.http import StreamingHttpResponse

urlpatterns = [
    path('', views.dashboard, name='index'),
    path('twitter',views.twitter,name='twitter'),
    path('dashboard/', views.dashboard, name='dashboard'),
    re_path(r'^customer_list/(?P<p_num>\d+|)?$', views.customer_list, name='customer_list'),

]

 