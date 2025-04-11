from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Question, Answer

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'body'] 


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['body']
