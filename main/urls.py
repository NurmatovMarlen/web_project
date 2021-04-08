
from django.contrib import admin
from django.urls import path, include

from .views import *

urlpatterns = [
   path('',MainPageView.as_view(),name='home'),
   path('category/<str:slug>/',CategoryDetailView.as_view(),name='category'),
   path('student-detail/<int:pk>/',StudentDetailview.as_view(),name='detail'),
   path('add-student/',add_student,name='add-student'),
   path('update-student/<int:pk>/',update_student,name='update-student'),
   path('delete-student/<int:pk>/',DeleteStudentView.as_view(),name='delete-student'),

]
