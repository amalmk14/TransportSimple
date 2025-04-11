from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import SignupForm, QuestionForm, AnswerForm
from .models import Question, Answer
from django.http import JsonResponse
from django.contrib.auth.models import User



def check_username(request):
    username = request.GET.get('username', None)
    exists = User.objects.filter(username__iexact=username).exists()
    return JsonResponse({'exists': exists})

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')


# @login_required
# def home(request):
#     questions = Question.objects.all().order_by('-created_at')
#     return render(request, 'home.html', {'questions': questions})

# @login_required
# def home(request):
#     view_type = request.GET.get('view', 'others')

#     if view_type == 'yours':
#         questions = Question.objects.filter(user=request.user).order_by('-created_at')
#     else:  
#         questions = Question.objects.exclude(user=request.user).order_by('-created_at')

#     return render(request, 'home.html', {'questions': questions, 'view_type': view_type})



# @login_required
# def post_question(request):
#     if request.method == 'POST':
#         form = QuestionForm(request.POST)
#         if form.is_valid():
#             question = form.save(commit=False)
#             question.user = request.user
#             question.save()
#             return redirect('home')
#     else:
#         form = QuestionForm()
#     return render(request, 'post_question.html', {'form': form})

# @login_required
# def view_question(request, pk):
#     question = get_object_or_404(Question, pk=pk)
#     answers = Answer.objects.filter(question=question)
#     return render(request, 'view_question.html', {'question': question, 'answers': answers})

# @login_required
# def answer_question(request, pk):
#     question = get_object_or_404(Question, pk=pk)
#     if request.method == 'POST':
#         form = AnswerForm(request.POST)
#         if form.is_valid():
#             answer = form.save(commit=False)
#             answer.user = request.user
#             answer.question = question
#             answer.save()
#             return redirect('view_question', pk=question.pk)
#     else:
#         form = AnswerForm()
#     return render(request, 'answer_question.html', {'form': form, 'question': question})

@login_required
def post_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user
            question.save()
    return redirect(request.META.get('HTTP_REFERER', 'home'))  # Redirect back


def home(request):
    view_type = request.GET.get('view', 'others')
    question_form = QuestionForm()

    if view_type == 'yours':
        questions = Question.objects.filter(user=request.user).order_by('-created_at')
    else:
        questions = Question.objects.exclude(user=request.user).order_by('-created_at')

    return render(request, 'home.html', {
        'questions': questions,
        'view_type': view_type,
        'question_form': question_form
    })

def view_question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    answers = Answer.objects.filter(question=question)
    question_form = QuestionForm()
    return render(request, 'view_question.html', {
        'question': question,
        'answers': answers,
        'question_form': question_form
    })

def answer_question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.user = request.user
            answer.question = question
            answer.save()
            return redirect('view_question', pk=question.pk)
    else:
        form = AnswerForm()

    question_form = QuestionForm()
    return render(request, 'answer_question.html', {
        'form': form,
        'question': question,
        'question_form': question_form
    })

@login_required
def delete_question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.user == question.user:
        question.delete()
    return redirect('home')

@login_required
def delete_answer(request, pk):
    answer = get_object_or_404(Answer, pk=pk)
    question_pk = answer.question.pk
    if request.user == answer.user:
        answer.delete()
    return redirect('view_question', pk=question_pk)


@login_required
def toggle_like_answer(request, pk):
    answer = get_object_or_404(Answer, pk=pk)
    user = request.user
    if user in answer.likes.all():
        answer.likes.remove(user)
    else:
        answer.likes.add(user)
    return redirect('view_question', pk=answer.question.pk)