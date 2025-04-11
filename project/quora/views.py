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

def check_email(request):
    email = request.GET.get('email', None)
    exists = User.objects.filter(email__iexact=email).exists()
    return JsonResponse({'exists': exists})

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('quora:home')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('quora:home')
#     return render(request, 'login.html')


def login_view(request):
    if request.method == 'POST':
        identifier = request.POST['username']  
        password = request.POST['password']
        try:
            user_obj = User.objects.get(email__iexact=identifier)
            username = user_obj.username
        except User.DoesNotExist:
            username = identifier 

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('quora:home')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('quora:login')



@login_required
def post_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user
            question.save()
    return redirect(request.META.get('HTTP_REFERER', 'quora:home'))  # Redirect back


from .models import Question, QuestionPass

@login_required
def home(request):
    view_type = request.GET.get('view', 'others')
    question_form = QuestionForm()

    if view_type == 'yours':
        questions = Question.objects.filter(user=request.user).order_by('-created_at')
    else:
        passed_question_ids = QuestionPass.objects.filter(user=request.user).values_list('question_id', flat=True)
        reported_question_ids = QuestionReport.objects.filter(user=request.user).values_list('question_id', flat=True)

        questions = Question.objects.exclude(user=request.user)\
            .exclude(id__in=passed_question_ids)\
            .exclude(id__in=reported_question_ids)\
            .order_by('-created_at')

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
            return redirect('quora:view_question', pk=question.pk)
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
    return redirect('quora:home')

@login_required
def delete_answer(request, pk):
    answer = get_object_or_404(Answer, pk=pk)
    question_pk = answer.question.pk
    if request.user == answer.user:
        answer.delete()
    return redirect('quora:view_question', pk=question_pk)


@login_required
def like_unlike_answer(request, pk):
    answer = get_object_or_404(Answer, pk=pk)
    user = request.user
    if user in answer.likes.all():
        answer.likes.remove(user)
    else:
        answer.likes.add(user)
    return redirect('quora:view_question', pk=answer.question.pk)


from .models import Question, QuestionPass, QuestionReport

@login_required
def pass_question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    QuestionPass.objects.get_or_create(user=request.user, question=question)
    return redirect('quora:home')


@login_required
def report_question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    report, created = QuestionReport.objects.get_or_create(user=request.user, question=question)
    if QuestionReport.objects.filter(question=question).count() >= 5:
        question.delete()
    return redirect('quora:home')