from django.urls import path
from . import views

app_name = 'quora'

urlpatterns = [
    path('', views.home, name='home'),
    path('check_username/', views.check_username, name='check_username'),
    path('check_email/', views.check_email, name='check_email'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('question/new/', views.post_question, name='post_question'),
    path('question/<int:pk>/', views.view_question, name='view_question'),
    path('question/<int:pk>/answer/', views.answer_question, name='answer_question'),
    path('answer/<int:pk>/like-unlike/', views.like_unlike_answer, name='like_unlike_answer'),
    path('question/delete/<int:pk>/', views.delete_question, name='delete_question'),
    path('answer/delete/<int:pk>/', views.delete_answer, name='delete_answer'),
    path('question/<int:pk>/pass/', views.pass_question, name='pass_question'),
    path('question/<int:pk>/report/', views.report_question, name='report_question'),



]
