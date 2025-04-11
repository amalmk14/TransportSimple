from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('ajax/check_username/', views.check_username, name='check_username'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('question/new/', views.post_question, name='post_question'),
    path('question/<int:pk>/', views.view_question, name='view_question'),
    path('question/<int:pk>/answer/', views.answer_question, name='answer_question'),
    path('answer/<int:pk>/like-toggle/', views.toggle_like_answer, name='toggle_like_answer'),
    path('question/delete/<int:pk>/', views.delete_question, name='delete_question'),
    path('answer/delete/<int:pk>/', views.delete_answer, name='delete_answer'),


]
