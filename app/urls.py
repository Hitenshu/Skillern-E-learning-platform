from django.contrib import admin
from django.urls import path 

from . import views

urlpatterns = [
    path('',views.home , name='home'),
    path('register/', views.register , name='register'),
    path('login/', views.login_view , name='login'),
    path('logout', views.logout , name='logout'),
    path('course/<slug:slug>',views.course_page , name='course_page'),
    path('my_course',views.my_course , name='my_course'),
    path('enroll/<slug:slug>',views.enroll , name='enroll'),
    path('verify_payment',views.verify_payment , name='verify_payment'),
    path('video/<int:video_id>/complete/', views.mark_video_completed, name='mark_video_completed'),
    path('certificate/<int:course_id>/', views.generate_certificate, name='generate_certificate'),
    path('about',views.about , name='about'),
    path('search',views.search , name='search'),

]


